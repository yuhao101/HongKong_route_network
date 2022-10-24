import os
from tqdm import tqdm
import pickle
import json
import csv
import sys


def generate_route_lat_lng(route_file, node_file):
    route_info = pickle.load(open(route_file, 'rb'))
    with open('./hongkong/node_json.json', 'r', encoding='utf-8') as file:
        id_lng_lat = json.load(file)
    route = []
    for i in range(len(route_info)):
        temp_route = []
        for node in route_info.iloc[i]['itinerary_segment_dis_list']:
            if str(node) in list(id_lng_lat.keys()):
                temp_route.append(id_lng_lat[str(node)])
            else:
                print(node)
        route.append(temp_route)
    return route


def generate_car_csv(all_route):
    route_file = open('./hongkong/route.csv', 'w')
    route_csv = csv.writer(route_file)
    route_csv.writerow(['geometry'])
    for s_route in all_route:
        temp_lat_lng = []
        for item in s_route:
            temp_lat_lng.append([item[1],item[0]])
        temp_route = {
            "type": "LineString",
            "coordinates": temp_lat_lng
        }
        route_csv.writerow([json.dumps(temp_route)])


def generate_route_time(record_path):
    records = pickle.load(open(record_path, 'rb'))
    routes = {}
    routes['data'] = []
    driver_cruising = {}
    length = 0
    for record in tqdm(records):
        length += 1
        # if length == 100:
        #     break
        for key in record:
            driver = record[key]
            if isinstance(driver[0], list):
                if key in driver_cruising.keys():
                    temp_time = driver_cruising[key][0]
                    temp_time.append(driver[0][-1])
                    temp_coordinate = driver_cruising[key][1]
                    temp_coordinate.append([driver[0][0], driver[0][1]])
                    temp_type = 0.0
                    routes['data'].append({
                        'time_list': temp_time,
                        'traj_list': temp_coordinate,
                        'type': temp_type
                    })
                    driver_cruising[key] = [[], []]
                temp_time = []
                temp_coordinate = []
                temp_type = 2.0
                flag = True
                for position in driver:
                    temp_time.append(position[-1])
                    temp_coordinate.append([position[0], position[1]])
                    if position[-2] == 1.0 and flag:
                        routes['data'].append({
                            'time_list': temp_time,
                            'traj_list': temp_coordinate,
                            'type': temp_type
                        })
                        temp_type = 1.0
                        temp_coordinate = [[position[0], position[1]]]
                        temp_time = [position[-1]]
                        flag = False
                routes['data'].append({
                    'time_list': temp_time,
                    'traj_list': temp_coordinate,
                    'type': temp_type
                })
            else:
                if key not in driver_cruising.keys():
                    driver_cruising[key] = [[driver[-1]], [[driver[0], driver[1]]]]
                else:
                    driver_cruising[key][0].append(driver[-1])
                    driver_cruising[key][1].append([driver[0], driver[1]])
    file = open('./hongkong/simulator_animation.json', 'w')
    file.write(json.dumps(routes, indent=1))


def calculate_metrics(record_path):
    records = pickle.load(open(record_path, 'rb'))
    order = pickle.load(open('./hongkong/hongkong_processed_order.pickle', 'rb'))
    order_num_time = {}
    matched_rate_time = {}
    current_num = 0
    matched_num = 0
    driver_no_cruising_time = {}
    for i in range(36000, 79200, 5):
        for j in range(0, 5):
            if (i+j) in order.keys():
                current_num += len(order[i+j])
        order_num_time[i] = current_num
    for i, time in enumerate(tqdm(records)):
        for driver in time:
            if driver not in driver_no_cruising_time.keys():
                driver_no_cruising_time[driver] = [set(), set()]
            if isinstance(time[driver][0], list):
                record = time[driver]
                matched_num += 1
                for single_record in record:
                    if single_record[-2] == 1.0:
                        for second in range(i*5+36000, int(single_record[-1])):
                            driver_no_cruising_time[driver][0].add(second)
                        for second in range(int(single_record[-1]), int(record[-1][-1])):
                            driver_no_cruising_time[driver][1].add(second)
                        break
        matched_rate_time[i*5+36000] = [matched_num/order_num_time[i*5+36000], matched_num, order_num_time[i*5+36000]-matched_num]
    for key in tqdm(matched_rate_time.keys()):
        pickup_count = 0
        delivery_count = 0
        cruising_count = 0
        for driver in driver_no_cruising_time.keys():
            if key in driver_no_cruising_time[driver][0]:
                pickup_count += 1
            elif key in driver_no_cruising_time[driver][1]:
                delivery_count += 1
            else:
                cruising_count += 1
        matched_rate_time[key].append(pickup_count/2000)
        matched_rate_time[key].append(delivery_count/2000)
        matched_rate_time[key].append(cruising_count/2000)
    file = open('./hongkong/simulator_metrics.json', 'w')
    file.write(json.dumps(matched_rate_time, indent=1))


def generate_driver_heatmap():
    heatMap = []
    driver = pickle.load(open('./hongkong/driver_info.pickle', 'rb')).head(2000)
    for i in range(2000):
        driver_coordinate = driver.loc[i, ['lng','lat']]
        heatMap.append([driver_coordinate['lng'],driver_coordinate['lat']])
    file = open('./hongkong/headMap.json', 'w')
    file.write(json.dumps(heatMap, indent=1))


def generate_order_heatmap():
    heatMap = []
    order_info = pickle.load(open('./hongkong/hongkong_processed_order.pickle', 'rb'))
    for i in range(36000, 79200):
        if i in order_info.keys():
            for order in order_info[i]:
                heatMap.append([order[3], order[2]])
    file = open('./hongkong/hongkong_order_headMap.json', 'w')
    file.write(json.dumps(heatMap, indent=1))


def generate_driver_info_by_records(record_path):
    heatMap = []
    driver_coordinate = {}
    records = pickle.load(open(record_path, 'rb'))
    for record in tqdm(records):
        for driver in record.keys():
            if isinstance(record[driver][0], list):
                driver_coordinate[driver] = [record[driver][-1][1], record[driver][-1][0]]
            else:
                driver_coordinate[driver] = [record[driver][1], record[driver][0]]
    for value in driver_coordinate.values():
        heatMap.append(value)
    file = open('./hongkong/driver_after_delivery_headMap.json', 'w')
    file.write(json.dumps(heatMap, indent=1))


def generate_order_info_by_records(record_path):
    heatMap = []
    order_origin_info = {}
    order_info = pickle.load(open('./hongkong/hongkong_processed_order.pickle', 'rb'))
    for i in tqdm(range(36000, 79200)):
        if i in order_info.keys():
            for order in order_info[i]:
                order_origin_info[order[0]] = [order[3], order[2]]
    records = pickle.load(open(record_path, 'rb'))
    finished_order = set()
    for record in tqdm(records):
        for driver in record.keys():
            if isinstance(record[driver][0], list):
                finished_order.add(record[driver][0][2])

    for key in order_origin_info.keys():
        if key in finished_order:
            continue
        heatMap.append(order_origin_info[key])
    print(len(heatMap))
    print(len(order_origin_info))
    file = open('./hongkong/order_after_delivery_cruising_headMap.json', 'w')
    file.write(json.dumps(heatMap, indent=1))


def extract_driver_record(record_path):
    records = pickle.load(open(record_path, 'rb'))
    driver_num = 5
    driver_records = {}
    driver_temp = {}
    for id in range(driver_num):
        driver_records[str(id)] = []
        driver_temp[str(id)] = []
    for record in tqdm(records):
        for driver in record:
            if isinstance(record[driver][0], list):
                if driver in driver_records.keys():
                    driver_records[driver].append({
                        "geometry": {
                            "type": "LineString",
                            "coordinates": driver_temp[driver]
                        },
                        "color": 'yellow'
                    })
                    single_record = record[driver]
                    temp_coordinates = []
                    for coor in single_record:
                        temp_coordinates.append([coor[0], coor[1]])
                        if coor[-2] == 1.0:
                            driver_records[driver].append({
                                "geometry": {
                                    "type": "LineString",
                                    "coordinates": temp_coordinates
                                },
                                "color": 'green'
                            })
                            temp_coordinates = [[coor[0], coor[1]]]
                    driver_records[driver].append({
                        "geometry": {
                            "type": "LineString",
                            "coordinates": temp_coordinates
                        },
                        "color": 'red'
                    })
                    driver_temp[driver] = []
            else:
                if driver in driver_temp.keys():
                    driver_temp[driver].append([record[driver][0], record[driver][1]])
    print(driver_records)
    file = open('./hongkong/animation_car_line_test.json', 'w')
    file.write(json.dumps(driver_records['0'], indent=1))


def extract_one_driver_record(record_path):
    records = pickle.load(open(record_path, 'rb'))
    driver_records = {
        '5': {
            'geometry': {
                'type': 'LineString',
                'coordinates': []
            }
        }
    }
    for record in tqdm(records):
        for driver in record:
            if isinstance(record[driver][0], list):
                if driver in driver_records.keys():
                    for coor in record[driver]:
                        driver_records[driver]['geometry']['coordinates'].append([coor[0], coor[1]])
            else:
                if driver in driver_records.keys():
                    driver_records[driver]['geometry']['coordinates'].append([record[driver][0], record[driver][1]])
    print(driver_records)
    file = open('./hongkong/animation_car_line.json', 'w')
    file.write(json.dumps(driver_records, indent=1))


def calculate_metrics_passenger(record_path):
    records = pickle.load(open(record_path, 'rb'))
    order = pickle.load(open('./hongkong/hongkong_processed_order.pickle', 'rb'))
    order_to_time = {}
    prematching_time = {}
    for i in range(36000, 79200, 5):
        for j in range(0, 5):
            if (i + j) in order.keys():
                for single_order in order[i+j]:
                    order_to_time[single_order[0]] = i

    prematching_time_temp_list = []
    postmatching_time_temp_list = []
    for i, time in enumerate(tqdm(records)):
        temp_pre = []
        temp_post = []
        if prematching_time_temp_list == []:
            prematching_time[i*5+36000] = [0, 0]
        else:
            if len(prematching_time_temp_list) < 361:
                if (sum(len(i) for i in prematching_time_temp_list)) == 0:
                    prematching_time[i * 5 + 36000] = [0]
                else:
                    prematching_time[i*5+36000] = [sum(sum(i) for i in prematching_time_temp_list)/(sum(len(i) for i in prematching_time_temp_list))]
                if (sum(len(i) for i in postmatching_time_temp_list)) == 0:
                    prematching_time[i * 5 + 36000].append(0)
                else:
                    prematching_time[i*5+36000].append(sum(sum(i) for i in postmatching_time_temp_list)/(sum(len(i) for i in postmatching_time_temp_list)))
            else:
                prematching_time[i * 5 + 36000] = [
                    sum(sum(i) for i in prematching_time_temp_list[1:]) / (sum(len(i) for i in prematching_time_temp_list[1:]))]
                prematching_time[i * 5 + 36000].append(sum(sum(i) for i in postmatching_time_temp_list[1:]) / (
                    sum(len(i) for i in postmatching_time_temp_list[1:])))
                prematching_time_temp_list = prematching_time_temp_list[1:]
                postmatching_time_temp_list = postmatching_time_temp_list[1:]
        for driver in time:
            if isinstance(time[driver][0], list):
                record = time[driver]
                matching_time = record[0][-1]
                pickup_end_time = 79200
                for single_record in record:
                    if single_record[-2] == 1:
                        pickup_end_time = min(single_record[-1], pickup_end_time)
                        break
                temp_pre.append(matching_time - order_to_time[record[0][2]])
                temp_post.append(pickup_end_time - matching_time)
        prematching_time_temp_list.append(temp_pre)
        postmatching_time_temp_list.append(temp_post)

    file = open('./hongkong/simulator_metrics_passenger.json', 'w')
    file.write(json.dumps(prematching_time, indent=1))


def generate_od_data(record_path):
    order_pair = []
    order = pickle.load(open(record_path, 'rb'))
    for i in range(36000, 79200):
        if i in order.keys():
            for single_order in order[i]:
                start_point = (single_order[2], single_order[3])
                end_point = (single_order[5], single_order[6])
                order_pair.append([i, start_point, end_point])

    file = open('./hongkong/order_pair.json', 'w')
    file.write(json.dumps(order_pair, indent=1))


def generate_panel_data():
    metrics = json.load(open('./hongkong/simulator_metrics.json'))
    hour_metrics = dict()
    time_interval = 3600
    for t in range(36000, 79200, 5):
        hour = int(t/time_interval)
        values = metrics[str(t)]
        if hour not in hour_metrics.keys():
            hour_metrics[hour] = [0] * 8
            for j in range(6):
                hour_metrics[hour][j] += values[j]
        else:
            for j in range(6):
                hour_metrics[hour][j] += values[j]
    new_metrics = json.load(open('./hongkong/simulator_metrics_passenger.json'))
    for t in range(36000, 79200, 5):
        hour = int(t / time_interval)
        values = new_metrics[str(t)]
        for j in range(6, 8):
            hour_metrics[hour][j] += values[j-6]
    # print(hour_metrics)
    total_add_count = time_interval/5
    for t in hour_metrics.keys():
        hour_metrics[t][0] = hour_metrics[t][0]/total_add_count*100
        hour_metrics[t][3] = hour_metrics[t][3]/total_add_count*100
        hour_metrics[t][4] = hour_metrics[t][4]/total_add_count*100
        hour_metrics[t][5] = hour_metrics[t][5]/total_add_count*100
        hour_metrics[t][6] = hour_metrics[t][6]/total_add_count
        hour_metrics[t][7] = hour_metrics[t][7]/total_add_count
        hour_metrics[t][1] = metrics[str((t+1)*time_interval-5)][1]
        hour_metrics[t][2] = metrics[str((t+1)*time_interval-5)][2]
    result = []
    for i in range(8):
        temp_result = []
        for value in hour_metrics.values():
            temp_result.append(value[i])
        result.append(temp_result)
    print(result)
    json.dump(result, open('./hongkong/panel.json', 'w'), indent=1)


def generate_od_by_time():
    order_pair = {}
    order = pickle.load(open('./hongkong/hongkong_processed_order.pickle', 'rb'))
    for i in range(36000, 39200):
        if i in order.keys():
            for single_order in order[i]:
                start_point = (single_order[2], single_order[3])
                end_point = (single_order[5], single_order[6])
                order_pair[i] = ([start_point, end_point])

    file = open('./hongkong/order_pair_by_time_test.json', 'w')
    file.write(json.dumps(order_pair, indent=1))


def generate_od_by_two():
    order = json.load(open('./hongkong/order_pair.json', 'r'))
    res = {'morning':[],'evening':[]}
    morning_start = 36000
    evening_start = 72000
    temp_res = []
    time_interval = 600
    for time in order:
        if time[0] <= 43200:
            if time[0] < morning_start + time_interval:
                temp_res.append([time[1],time[2]])
            else:
                res['morning'].append(temp_res)
                temp_res = []
                morning_start += time_interval
        elif time[0] >= 72000:
            if time[0] < evening_start + time_interval:
                temp_res.append([time[1],time[2]])
            else:
                res['evening'].append(temp_res)
                temp_res = []
                evening_start += time_interval
    file = open('./hongkong/order_pair_by_time.json', 'w')
    file.write(json.dumps(res, indent=1))


def generate_od_node_by_time():
    order = json.load(open('./hongkong/simulator_animation.json', 'r'))['data']
    res = {'morning': [], 'evening': []}
    for record in tqdm(order):
        time = record['time_list']
        traj = record['traj_list']
        if record['type'] != 1.0:
            continue
        if time[0] <= 43200:
            res['morning'].append({'time': time, 'traj': traj})
        elif time[0] >= 72000:
            res['evening'].append({'time': time, 'traj': traj})
    file = open('./hongkong/order_node_by_time.json', 'w')
    file.write(json.dumps(res, indent=1))


if __name__ == '__main__':
    # record_path = './hongkong/'
    # record_file = os.listdir(record_path)
    # print(record_file)
    # for file in record_file[1:]:
    #     generate_route_time(record_path+file)
    #     calculate_metrics(record_path+file)
    #     # extract_one_driver_record(record_path+file)
    #     calculate_metrics_passenger(record_path+file)
    #     generate_od_data(record_path+file)
    # path = './hongkong/records_max_distance_1_time_interval_5.pickle'
    # generate_route_time(path)
    # calculate_metrics(path)
    # calculate_metrics_passenger(path)

    generate_panel_data()
    # generate_od_data('./hongkong/hongkong_processed_order.pickle')
    # print('end')
    # generate_od_by_two()
    # generate_od_node_by_time()
    # generate_order_heatmap()
    # generate_driver_heatmap()
    # generate_order_heatmap()
    # record_path = './hongkong/record/records_driver_num_2000_cruising.pickle'
    # generate_order_info_by_records(record_path)
    # generate_od_by_time()


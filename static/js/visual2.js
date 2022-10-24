var panel =
[[87.67507920138917, 83.72116350537964, 80.73084703282257, 78.44691165555527, 76.27953577942014, 74.97291357301765, 74.12266373095629, 74.04849682601375, 71.58355393415839, 67.96871768191636, 65.7036031812717, 63.78138027328598], [5479, 10609, 15682, 20573, 25124, 29361, 33387, 37249, 40387, 43559, 46595, 49099], [1000, 2269, 4206, 6057, 8191, 10040, 11638, 13539, 17676, 21772, 25347, 29189], [17.440416666666668, 15.228749999999971, 14.383263888888873, 14.085277777777772, 12.786041666666703, 12.751041666666662, 12.454236111111141, 12.145486111111126, 10.649513888888885, 11.248124999999993, 10.909444444444425, 9.67020833333333], [37.78833333333335, 45.96965277777771, 47.044583333333314, 44.989236111111, 45.613958333333265, 42.79861111111119, 41.18416666666672, 39.068541666666704, 40.72055555555557, 43.64375000000003, 42.682222222222265, 38.852638888888876], [44.77125000000001, 38.80159722222222, 38.57215277777774, 40.92548611111114, 41.59999999999992, 44.450347222222156, 46.36159722222225, 48.78597222222227, 48.62993055555565, 45.10812499999982, 46.408333333333346, 51.4771527777778], [28.996780989874317, 39.956710117035364, 54.379181734935, 56.61584715881585, 59.95308988980468, 55.037526764875295, 56.125727506455426, 59.82041032610322, 71.00372482538508, 77.93777374144919, 74.08755148041234, 63.03465765972018], [248.28709303468528, 213.82874560984038, 209.3717869285888, 209.18050187953435, 202.56017553985868, 214.77596975183772, 228.86343898170122, 221.26660486227414, 240.7856898751263, 249.2193668876215, 248.9513516843888, 241.96300032182083]]
option1 = {
  textStyle: {
    color: '#ffffff'
  },
  tooltip: {
    trigger: 'axis',
    axisPointer: {
      type: 'shadow'
    }
  },
  legend: {textStyle: {
    color: '#ffffff',
          fontSize:10,
  },
      top:25,
  },
  grid: {
    left: '3%',
    right: '4%',
    bottom: '3%',
    containLabel: true
  },
  xAxis: [
    {
      type: 'category',
      data: ['11:00', '12:00']
    }
  ],
  yAxis: [
    {
      type: 'value',

    }
  ],
    color: ['#009883', '#e66922'],
  series: [
    {
      name: 'Completed orders',
      type: 'bar',
      emphasis: {
        focus: 'series'
      },
      data: panel[1].slice(0,2)
    },
    {
      name: 'Cancelled orders',
      type: 'bar',
      emphasis: {
        focus: 'series'
      },
      data: panel[2].slice(0,2)
    }
  ]
};
option2 = {
  textStyle: {
    color: '#ffffff'
  },
  tooltip: {
    trigger: 'axis',
    axisPointer: {
      type: 'shadow'
    }
  },
  legend: {textStyle: {
    color: '#ffffff',
          fontSize:10,
  },
      top:25,},
  grid: {
    left: '3%',
    right: '4%',
    bottom: '3%',
    containLabel: true
  },
  xAxis: [
    {
      type: 'category',
      data: ['11:00', '12:00']
    }
  ],
  yAxis: [
    {
      type: 'value',
        axisLabel: {
        formatter: '{value} %'
      }
    }
  ],
    color: ['#845EC2', '#D65DB1', '#F9F871'],
  series: [
    {
      name: 'Pickup',
      type: 'bar',
      emphasis: {
        focus: 'series'
      },
      data: panel[3].slice(0,2)
    },
    {
      name: 'Delivery',
      type: 'bar',
      emphasis: {
        focus: 'series'
      },
      data: panel[4].slice(0,2)
    },
    {
      name: 'Idle',
      type: 'bar',
      emphasis: {
        focus: 'series'
      },
      data: panel[5].slice(0,2)
    }
  ]
};
option21 = {
  textStyle: {
    color: '#ffffff'
  },
  tooltip: {
    trigger: 'axis',
    axisPointer: {
      type: 'shadow'
    }
  },
  legend: {textStyle: {
    color: '#ffffff',
          fontSize:10,
  },top:25,
  },
  grid: {
    left: '3%',
    right: '4%',
    bottom: '3%',
    containLabel: true
  },
  xAxis: [
    {
      type: 'category',
      data: ['11:00', '12:00']
    }
  ],
  yAxis: [
    {
      type: 'value',
        axisLabel: {
        formatter: '{value} s'
      }
    }
  ],
    color: ['#F3C5FF', '#0081CF'],
  series: [
    {
      name: 'Waiting time for pickup',
      type: 'bar',
      emphasis: {
        focus: 'series'
      },
      data: panel[6].slice(0,2)
    },
    {
      name: 'Waiting time for matching',
      type: 'bar',
      emphasis: {
        focus: 'series'
      },
      data: panel[7].slice(0,2)
    }
  ]
};
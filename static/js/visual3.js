var panel =
[[0.9597400086400517, 0.9284936583391741, 0.9133551211368733, 0.922132681439626, 0.9253098993089535, 0.9324087819332454, 0.9243541331243148, 0.9220185780633982, 0.9147542616424984, 0.9156650110148477, 0.9226605959471905, 0.9279352252134632], [724, 1510, 2294, 3041, 3756, 4395, 4975, 5600, 6296, 7107, 7791, 8483], [45, 152, 203, 260, 285, 313, 432, 460, 610, 620, 628, 636], [0.06110069444444456, 0.07011736111111122, 0.073377777777778, 0.0712243055555558, 0.06874375000000021, 0.06603333333333329, 0.06250694444444431, 0.0605604166666666, 0.06517916666666687, 0.08003819444444461, 0.06641041666666679, 0.06784236111111125], [0.04908055555555558, 0.0890180555555557, 0.08430555555555583, 0.0831916666666669, 0.07833472222222236, 0.07129930555555554, 0.07452013888888896, 0.07085277777777799, 0.07849236111111134, 0.09836527777777745, 0.08075416666666685, 0.07927916666666701], [0.8898187500000011, 0.8408645833333304, 0.8423166666666673, 0.8455840277777776, 0.8529215277777796, 0.8626673611111136, 0.8629729166666695, 0.8685868055555566, 0.8563284722222215, 0.8215965277777758, 0.8528354166666676, 0.8528784722222238], [14.666161488669452, 30.768588376984376, 44.62806580798934, 33.06717598215866, 32.067110989858016, 22.768689861388395, 57.01594734952137, 46.98370468405998, 59.07011382829559, 23.273276793057832, 12.126427425314324, 11.343769321400908], [702.0551411084369, 677.6501767423256, 686.3203139387223, 697.3660211288479, 695.1071752486805, 784.8609795930947, 736.0293962314984, 685.8039720662406, 712.5524316907916, 664.731697196513, 683.5312223501576, 631.9105746564428]]

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
    color: '#ffffff'
  },},
  grid: {
    left: '3%',
    right: '4%',
    bottom: '3%',
    containLabel: true
  },
  xAxis: [
    {
      type: 'category',
      data: ['10:00', '12:00', '14:00', '16:00', '18:00', '20:00', '22:00']
    }
  ],
  yAxis: [
    {
      type: 'value'
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
      data: panel[1].slice(0,7),
    },
    {
      name: 'Cancelled orders',
      type: 'bar',
      emphasis: {
        focus: 'series'
      },
      data: panel[2].slice(0,7)
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
    color: '#ffffff'
  },},
  grid: {
    left: '3%',
    right: '4%',
    bottom: '3%',
    containLabel: true
  },
  xAxis: [
    {
      type: 'category',
      data: ['10:00', '12:00', '14:00', '16:00', '18:00', '20:00', '22:00']
    }
  ],
  yAxis: [
    {
      type: 'value'
    }
  ],
    color: ['#845EC2', '#D65DB1', '#F9F871'],
  series: [
    {
      name: 'Pickup ratio',
      type: 'bar',
      emphasis: {
        focus: 'series'
      },
      data: panel[3].slice(0,7),
    },
    {
      name: 'Delivery ratio',
      type: 'bar',
      emphasis: {
        focus: 'series'
      },
      data: panel[4].slice(0,7)
    },
    {
      name: 'Idle ratio',
      type: 'bar',
      emphasis: {
        focus: 'series'
      },
      data: panel[5].slice(0,7)
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
    color: '#ffffff'
  },},
  grid: {
    left: '3%',
    right: '4%',
    bottom: '3%',
    containLabel: true
  },
  xAxis: [
    {
      type: 'category',
      data: ['10:00', '12:00', '14:00', '16:00', '18:00', '20:00', '22:00']
    }
  ],
  yAxis: [
    {
      type: 'value'
    }
  ],
    color: ['#F3C5FF', '#0081CF'],
  series: [
    {
      name: 'Average passenger pickup time',
      type: 'bar',
      emphasis: {
        focus: 'series'
      },
      data: panel[6].slice(0,7),
    },
    {
      name: 'Average passenger waiting time',
      type: 'bar',
      emphasis: {
        focus: 'series'
      },
      data: panel[7].slice(0,7)
    }
  ]
};
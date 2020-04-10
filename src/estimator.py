
def estimator(data):
  '''
  Method for impact estimation on the covid_19 pandemic based on calculations
  and studys by Havard Medical School and Massachusetts General Hospital

  Args:
      Dictionary data such as the example below.
      {
        region: {
        name: "Africa",
        avgAge: 19.7,
        avgDailyIncomeInUSD: 5,
        avgDailyIncomePopulation: 0.71
        },
        periodType: "days",
        timeToElapse: 58,
        reportedCases: 674,
        population: 66622705,
        totalHospitalBeds: 1380614
      }
  '''
  #original data storage
  originalData = data

  #Calculations for Currently infected

  currentlyInfectedImpact = data['reportedCases'] * 10
  currentlyInfectedSeverImpact = data['reportedCases'] * 50

  
  # Start of calculations for infections by requested time. factoring in one will use
  # days,weeks and months

  if data['periodType'] is "weeks":
    data['timeToElapse'] = data['timeToElapse'] * 7

  elif data['periodType'] is "months":
    data['timeToElapse'] = data['timeToElapse'] * 30

  else:
    pass

  powerNumber = int(data['timeToElapse']/3)
  infectionsByRequestedTimeImpact = int(currentlyInfectedImpact * (2**powerNumber))
  infectionsByRequestedTimeSeverImpact = int(currentlyInfectedSeverImpact * (2**powerNumber))

  #Start of calculations for severcases of infection that will require hospitalization

  severeCasesByRequestedTimeImpact = int(0.15 * infectionsByRequestedTimeImpact)
  severeCasesByRequestedTimeSevereImpact = int(0.15 * infectionsByRequestedTimeSeverImpact)

  #Start of calculation for number of hospital beds available for covid_19 Patients at requested time
  
  availableBeds = int(0.35 * data['totalHospitalBeds'])
  hospitalBedsByRequestedTimeImpact = availableBeds - severeCasesByRequestedTimeImpact
  hospitalBedsByRequestedTimeSeverImpact = availableBeds - severeCasesByRequestedTimeSevereImpact

  # data to be returned inform of a dictionary
  data = {'data':{'region': {
                              'name': originalData['region']['name'],
                              'avgAge': originalData['region']['avgAge'],
                              'avgDailyIncomeInUSD': originalData['region']['avgDailyIncomeInUSD'],
                              'avgDailyIncomePopulation': originalData['region']['avgDailyIncomePopulation']
                            },
                  'periodType': originalData['periodType'],
                  'timeToElapse': originalData['timeToElapse'],
                  'reportedCases': originalData['reportedCases'],
                  'population': originalData['population'],
                  'totalHospitalBeds': originalData['totalHospitalBeds']
          },
          'estimate':{
                        'impact':{'currentlyInfected': currentlyInfectedImpact,
                                'infectionsByRequestedTime': infectionsByRequestedTimeImpact,
                                'severeCasesByRequestedTime': severeCasesByRequestedTimeImpact,
                                'hospitalBedsByRequestedTime': hospitalBedsByRequestedTimeImpact
                        },

                        'severImpact':{'currentlyInfected':currentlyInfectedSeverImpact,
                                      'infectionsByRequestedTime': infectionsByRequestedTimeSeverImpact,
                                      'severeCasesByRequestedTime':severeCasesByRequestedTimeSevereImpact,
                                      'hospitalBedsByRequestedTime': hospitalBedsByRequestedTimeSeverImpact
                        }
          }
  }

  return data

def estimator(data):
  '''
  Method for impact estimation on the covid_19 pandemic based on calculations
  and studys by Havard Medical School and Massachusetts General Hospital

  Args:
      Dictionary data such as the example below.
      {
        'region': {
        'name': "Africa",
        'avgAge': 19.7,
        'avgDailyIncomeInUSD': 4,
        'avgDailyIncomePopulation': 0.73
        },
        'periodType': "days",
        'timeToElapse': 38,
        'reportedCases': 2747,
        'population': 92931687,
        'totalHospitalBeds': 678874
      }
  '''
  #original data storage
  originalData = data

  #Calculations for Currently infected

  currentlyInfectedImpact = int(data['reportedCases'] * 10)
  currentlyInfectedSeverImpact = int(data['reportedCases'] * 50)


  # Start of calculations for infections by requested time. factoring in one will use
  # days,weeks and months

  if data['periodType'] == "weeks":
    data['timeToElapse'] = data['timeToElapse'] * 7

  elif data['periodType'] == "months":
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

  availableBeds = 0.35 * data['totalHospitalBeds']
  hospitalBedsByRequestedTimeImpact = int(availableBeds - severeCasesByRequestedTimeImpact)
  hospitalBedsByRequestedTimeSeverImpact = int(availableBeds - severeCasesByRequestedTimeSevereImpact)

  #Start of calculation for ICU cases

  casesForICUByRequestedTimeImpact = int(0.5 * infectionsByRequestedTimeImpact)
  casesForICUByRequestedTimeSeverImpact = int(0.5 * infectionsByRequestedTimeSeverImpact)

  #Ventilator Requirements
  casesForVentilatorsByRequestedTimeImpact = int(0.2 * infectionsByRequestedTimeImpact)
  casesForVentilatorsByRequestedTimeSeverImpact = int(0.2 * infectionsByRequestedTimeSeverImpact)

  #Economy loss calculation

  dollarsInFlightImpact = int((infectionsByRequestedTimeImpact * data['region']['avgDailyIncomePopulation'] * data['region']['avgDailyIncomeInUSD']) / data['timeToElapse'])*10
  dollarsInFlightSeverImpact = int((infectionsByRequestedTimeSeverImpact * data['region']['avgDailyIncomePopulation'] * data['region']['avgDailyIncomeInUSD']) / data['timeToElapse'])*10

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

                        'impact':{'currentlyInfected': currentlyInfectedImpact,
                                'infectionsByRequestedTime': infectionsByRequestedTimeImpact,
                                'severeCasesByRequestedTime': severeCasesByRequestedTimeImpact,
                                'hospitalBedsByRequestedTime': hospitalBedsByRequestedTimeImpact,
                                'casesForICUByRequestedTime': casesForICUByRequestedTimeImpact,
                                'casesForVentilatorsByRequestedTime':casesForVentilatorsByRequestedTimeImpact,
                                'dollarsInFlight': dollarsInFlightImpact
                        },

                        'severeImpact':{'currentlyInfected':currentlyInfectedSeverImpact,
                                      'infectionsByRequestedTime': infectionsByRequestedTimeSeverImpact,
                                      'severeCasesByRequestedTime':severeCasesByRequestedTimeSevereImpact,
                                      'hospitalBedsByRequestedTime': hospitalBedsByRequestedTimeSeverImpact,
                                      'casesForICUByRequestedTime': casesForICUByRequestedTimeSeverImpact,
                                      'casesForVentilatorsByRequestedTime':casesForVentilatorsByRequestedTimeSeverImpact,
                                      'dollarsInFlight': dollarsInFlightSeverImpact
                        }
  }

  return data
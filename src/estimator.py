from math import trunc
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

  currentlyInfectedImpact = trunc(data['reportedCases'] * 10)
  currentlyInfectedSeverImpact = trunc(data['reportedCases'] * 50)


  # Start of calculations for infections by requested time. factoring in one will use
  # days,weeks and months

  if data['periodType'] == "weeks":
    data['timeToElapse'] = data['timeToElapse'] * 7

  elif data['periodType'] == "months":
    data['timeToElapse'] = data['timeToElapse'] * 30

  else:
    pass

  powerNumber = trunc(data['timeToElapse']/3)
  infectionsByRequestedTimeImpact = trunc(currentlyInfectedImpact * (2**powerNumber))
  infectionsByRequestedTimeSeverImpact = trunc(currentlyInfectedSeverImpact * (2**powerNumber))

  #Start of calculations for severcases of infection that will require hospitalization

  severeCasesByRequestedTimeImpact = trunc(0.15 * infectionsByRequestedTimeImpact)
  severeCasesByRequestedTimeSevereImpact = trunc(0.15 * infectionsByRequestedTimeSeverImpact)

  #Start of calculation for number of hospital beds available for covid_19 Patients at requested time

  availableBeds = 0.35 * data['totalHospitalBeds']
  hospitalBedsByRequestedTimeImpact = trunc(availableBeds - severeCasesByRequestedTimeImpact)
  hospitalBedsByRequestedTimeSeverImpact = trunc(availableBeds - severeCasesByRequestedTimeSevereImpact)

  #Start of calculation for ICU cases

  casesForICUByRequestedTimeImpact = trunc(0.5 * infectionsByRequestedTimeImpact)
  casesForICUByRequestedTimeSeverImpact = trunc(0.5 * infectionsByRequestedTimeSeverImpact)

  #Ventilator Requirements
  casesForVentilatorsByRequestedTimeImpact = trunc(0.2 * infectionsByRequestedTimeImpact)
  casesForVentilatorsByRequestedTimeSeverImpact = trunc(0.2 * infectionsByRequestedTimeSeverImpact)

  #Economy loss calculation

  difImpact = infectionsByRequestedTimeImpact * data['region']['avgDailyIncomePopulation'] * data['region']['avgDailyIncomeInUSD'] * data['timeToElapse']
  difSI = infectionsByRequestedTimeSeverImpact * data['region']['avgDailyIncomePopulation'] * data['region']['avgDailyIncomeInUSD'] * data['timeToElapse']

  dollarsInFlightImpact = round(difImpact,2)
  dollarsInFlightSeverImpact = round(difSI,2)

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
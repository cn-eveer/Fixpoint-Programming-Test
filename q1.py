import os
from time import sleep
from datetime import datetime
from dotenv import load_dotenv

def main():

  # Load local .env file
  load_dotenv()

  # Load log data filename
  filename = os.getenv("FILE_NAME")
  if not len(filename):
    print("PLEASE ENTER FILENAME IN ENV FILE")
    exit()

  inputs = open(filename, "r")

  # Variables
  timeout_lists = {}
  recovered_lists = []

  # Read data by each line
  for item in inputs:

    data = item.split(",")

    # If timed out IP is present
    if len(timeout_lists):

      # Check if any timed out IP is recovered
      for ip in timeout_lists:

        t_data = timeout_lists[ip][0]

        # if time out IP is recovered
        if t_data[1] == data[1] and data[2][0] != '-':

          start,stop = datetime(int(str(t_data[0][0:4])),int(str(t_data[0][4:6])),int(t_data[0][6:8]),
            int(str(t_data[0][8:10])),int(str(t_data[0][10:12])),int(t_data[0][12:14])), datetime(int(str(data[0][0:4])),
            int(str(data[0][4:6])),int(data[0][6:8]),int(str(data[0][8:10])),int(str(data[0][10:12])),int(data[0][12:14]))

          # Total time taken to recover
          result = int((stop-start).total_seconds())

          # Information stored to recovered lists 
          # [ IP, IP timed out time, IP recovered time, time to recover ]
          recovered_lists.append([data[1],start,stop,result])

          # Remove IP from timed out IP list
          timeout_lists.pop(data[1])

          break

    # Check if IP timed out
    if data[2].strip('\n') == '-':

      try:
        timeout_lists[data[1]]
      except:
        timeout_lists[data[1]] = []

      # Add to time out IP lists
      timeout_lists[data[1]].append(data)

  print("\nUNRECOVERED IP\n")
  # Check if any IP is still timed out
  if len(timeout_lists) > 0:

    for item in timeout_lists:

      # Display IP addresss
      print(item,"not recovered since",timeout_lists[item][0][0])

  print("\nRECOVERED IP SESSION\n")
  # Check recovered IP session 
  if len(recovered_lists) > 0:

    for item in recovered_lists:

      # { IP } recovered at { when IP recovered } from { when IP timed out }
      # time-out { total time taken to recover }
      print(item[0],"recovered at",item[2],
        "from",item[1],"time-out:",item[3],"sec")

if __name__ == '__main__':
  main()
import os
from time import sleep
from datetime import datetime
from dotenv import load_dotenv

def main():

  load_dotenv()

  filename = os.getenv("FILE_NAME")
  num_error = int(os.getenv("ERROR_NUM"))

  inputs = open(filename, "r")

  timeout_lists = {}
  recovered_lists = []
  count_timeout = {}
  result_lists = {}
  ip_lists = []

  for item in inputs:
    data = item.split(",")

    if len(result_lists):
      for ip in result_lists:
        t_data = result_lists[ip]
        if t_data[1] == data[1] and data[2][0] != '-':

          start,stop = datetime(int(str(t_data[0][0:4])),int(str(t_data[0][4:6])),int(t_data[0][6:8]),
            int(str(t_data[0][8:10])),int(str(t_data[0][10:12])),int(t_data[0][12:14])), datetime(int(str(data[0][0:4])),
            int(str(data[0][4:6])),int(data[0][6:8]),int(str(data[0][8:10])),int(str(data[0][10:12])),int(data[0][12:14]))

          result = int((stop-start).total_seconds())
          if data[1] in ip_lists:
            recovered_lists.append([data[1],start,stop,result])
            ip_lists.remove(data[1])
          result_lists.pop(ip)
          timeout_lists.pop(ip)
          break

    if data[2].strip('\n') == '-':
      try:
        timeout_lists[data[1]]
      except:
        timeout_lists[data[1]] = []

      timeout_lists[data[1]].append(data)
      result_lists[data[1]] = timeout_lists[data[1]][0]

      if len(timeout_lists[data[1]]) >= num_error:
        if data[1] not in ip_lists:
          ip_lists.append(data[1])

  print("\nUNRECOVERED IP\n")
  if len(timeout_lists) > 0:
    for item in timeout_lists:
      print(item,"not recovered since",timeout_lists[item][0][0])

  print("\nRECOVERED IP SESSION\n")
  if len(recovered_lists) > 0:
    for item in recovered_lists:
      print(item[0],"recovered at",item[2],
        "from",item[1],"time-out:",item[3],"sec")

if __name__ == '__main__':
  main()
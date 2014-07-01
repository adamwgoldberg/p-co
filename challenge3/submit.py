#!/usr/bin/env python

import hashlib
import json
import os
from os import listdir
from os.path import isfile, join
import sys
import time
import urllib
import urllib2


def run_java_tests(input_file, output_file):
    os.system("javac Solution.java")
    os.system("java Solution %s %s" % (input_file, output_file))

def run_python_tests(input_file, output_file):
    os.system("python solution.py %s %s" % (input_file, output_file))

def run_cpp_tests(input_file, output_file):
    os.system('g++ Solution.cpp -o solution')
    cmd = './solution ' + input_file + ' ' + output_file
    os.system(cmd)


if __name__ == '__main__':
    if len(sys.argv) != 4:
        sys.stderr.write('You should only provide 3 arguments to the script.\n'
                         'Make sure there are no spaces in either your username or name.\n'
                         'See the "Submission Instructions/python" section of the doc for '
                         'more details.\n')
        sys.exit(2)

    name = sys.argv[1].strip()
    username = sys.argv[2].strip()
    language = sys.argv[3].strip()

    mypath = "input_files"
    inputfiles = [f for f in listdir(mypath) if isfile(join(mypath, f)) and f[:2] == 'in']
    inputfiles.sort()
    outputfiles = ["output_files/out.%s.txt" % i for i in range(0, len(inputfiles))]

    num_files = 5

    start = time.time()
    for index in range(0, num_files):
        input_file = "input_files/" + inputfiles[index]
        print "Running %s" % input_file
        if language == "python":
            run_python_tests(input_file, outputfiles[index])
        elif language == "java":
            run_java_tests(input_file, outputfiles[index])
        elif language == "cpp":
            run_cpp_tests(input_file, outputfiles[index])
    end = time.time()
    run_time = (end - start) * 1000

    try:
        m = hashlib.md5()
        solution = []
        for i in range(0, num_files):
            with open('output_files/out.' + str(i) + '.txt') as fd:
                solution.extend(map(str.strip, fd.readlines()))
        m.update(''.join(solution))
        m.update(name)
        solution_hash = m.hexdigest()

        solution_file = ""
        if language == "python":
            solution_file = 'solution.py'
        elif language == "java":
            solution_file = "Solution.java"
        elif language == "cpp":
            solution_file = "Solution.cpp"
        with open(solution_file) as fd:
            code_text = fd.readlines()

    except Exception:
        solution_hash = ''
        code_text = ''

    hostname = '172.16.0.232'
    url = 'http://%s:9000' % hostname
    post_dict = {'solution': solution_hash,
                 'run_time': run_time,
                 'username': username,
                 'name': name,
                 'language': language,
                 'code': json.dumps(code_text)}

    params = urllib.urlencode(post_dict)
    post_req = urllib2.Request(url)
    post_req.add_data(params)

    response = urllib2.urlopen(post_req)
    response_data = response.read()
    response.close()
    print response_data
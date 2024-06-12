import subprocess
j = None
with subprocess.Popen("python /home/ubuntu/Site/A37TextCNN/tc.py /home/ubuntu/Site/static/a37/recog_images/b5b8ca8d-4693-4fd3-8602-1a6346866aaf.jpeg",stdout=subprocess.PIPE,shell=True,) as p:
    p.wait()
    j = p.stdout.read()

print(j)
j = eval(j)
print(j)
j.update({"status":"200"})
print(j)

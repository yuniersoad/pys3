import os
import shutil

class Object:
	def __init__(self, name, isdir, size=0):
            self.name = name
            self.isdir = isdir
            self.size = size
	def __str__(self):
            return self.name if (not self.isdir) else self.name + "/"


def get_buckets(root_dir):
	return [name for name in os.listdir(root_dir) if os.path.isdir(os.path.join(root_dir, name))]

def delete_bucket(root_dir, bucket):
	shutil.rmtree(os.path.join(root_dir, bucket))

def delete_object(root_dir, bucket, path):
	full_path = os.path.join(root_dir, bucket, path)
	if (os.path.isdir(full_path)):
		os.rmdir(full_path)
	else:
		os.remove(full_path)

def get_objects(root_dir, bucket, prefix):
	base_dir = os.path.join(root_dir, bucket, prefix)
	result = []
	for name in os.listdir(base_dir):
            full_path = os.path.join(base_dir, name)
            if os.path.isdir(full_path):
                result.append(Object(name, True))
            else:
                result.append(Object(name, False, os.path.getsize(full_path)))
	return result


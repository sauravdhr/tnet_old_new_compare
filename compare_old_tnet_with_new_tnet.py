import shutil, os
import subprocess as sp
import operator
import threading
import get_edges as ge

def run_tnet_old_multiple_times(input_file, output_file, time = 100):
	temp_out_file = output_file + '.temp'
	edge_dict = {}
	source_count = {}
	result = open(output_file, 'w+')

	for t in range(time):
		cmd = 'python3 TNet/tnet.py {} {}'.format(input_file, temp_out_file)
		# os.system(cmd)
		child = sp.Popen(cmd.split(), stdout=sp.PIPE)
		out, err = child.communicate()
		if err:
			if verbose:
				print('Failure')
				print(err.decode('utf-8'))
			sys.exit(1)
		else:
			# print('Old', out.decode('utf-8'))
			output = out.decode('utf-8')
			source = output.rstrip().split(' ')[-1]
			source = source[8:]
			print(source)

			if source in source_count:
				source_count[source] += 1
			else:
				source_count[source] = 1

		e_list = []
		print(t,'Done')

		# Read result from temp_out_file and save to edge_dict
		f = open(temp_out_file)
		f.readline()
		for line in f.readlines():
			parts = line.rstrip().split('\t')
			edge = parts[0]+'->'+parts[1]

			if edge not in e_list:
				if edge in edge_dict:
					edge_dict[edge] += 1
				else:
					edge_dict[edge] = 1
				e_list.append(edge)

		f.close()
		os.remove(temp_out_file)
		os.remove(input_file + '.temp')
		os.remove(input_file + '.tnet.log')
		# break

	edge_dict = dict(sorted(edge_dict.items(), key=operator.itemgetter(1),reverse=True))
	# print(edge_dict)

	for x, y in edge_dict.items():
		# print(x, y)
		result.write('{}\t{}\n'.format(x, y))

	result.close()
	return source_count

def run_tnet_new_multiple_times(input_file, output_file, time = 100):
	temp_out_file = output_file + '.temp'
	edge_dict = {}
	source_count = {}
	result = open(output_file, 'w+')

	for t in range(time):
		cmd = 'python3 tnet.py {} {}'.format(input_file, temp_out_file)
		# os.system(cmd)
		child = sp.Popen(cmd.split(), stdout=sp.PIPE)
		out, err = child.communicate()
		if err:
			if verbose:
				print('Failure')
				print(err.decode('utf-8'))
			sys.exit(1)
		else:
			# print('New', out.decode('utf-8'))
			output = out.decode('utf-8')
			source = output.rstrip().split(' ')[-1]
			print(source)

			if source in source_count:
				source_count[source] += 1
			else:
				source_count[source] = 1

		e_list = []
		print(t,'Done')

		# Read result from temp_out_file and save to edge_dict
		f = open(temp_out_file)
		f.readline()
		for line in f.readlines():
			parts = line.rstrip().split('\t')
			edge = parts[0]+'->'+parts[1]

			if edge not in e_list:
				if edge in edge_dict:
					edge_dict[edge] += 1
				else:
					edge_dict[edge] = 1
				e_list.append(edge)

		f.close()
		os.remove(temp_out_file)
		# break

	edge_dict = dict(sorted(edge_dict.items(), key=operator.itemgetter(1),reverse=True))
	# print(edge_dict)

	for x, y in edge_dict.items():
		# print(x, y)
		result.write('{}\t{}\n'.format(x, y))

	result.close()
	return source_count

def run_tnet_old(times = 100):
	data_dir = 'dataset/'
	folders = next(os.walk(data_dir))[1]

	for folder in folders:
		print('Inside',folder)
		tree_file = data_dir + folder + '/RAxML_rooted_tree.tree'
		out_file = data_dir + folder + '/tnet_old_' + str(times) + '.tnet'
		# print(tree_file, out_file, times)
		run_tnet_old_multiple_times(tree_file, out_file, times)
		# break

def run_tnet_new(times = 100):
	data_dir = 'dataset/'
	folders = next(os.walk(data_dir))[1]

	for folder in folders:
		print('Inside',folder)
		tree_file = data_dir + folder + '/RAxML_rooted_tree.tree'
		out_file = data_dir + folder + '/tnet_new_' + str(times) + '.tnet'
		# print(tree_file, out_file, times)
		run_tnet_new_multiple_times(tree_file, out_file, times)
		break

def run_tnet_new_multithreaded(times = 100):
	data_dir = 'dataset/'
	folders = next(os.walk(data_dir))[1]
	t = []

	for folder in folders:
		# print('Inside',folder)
		tree_file = data_dir + folder + '/RAxML_rooted_tree.tree'
		out_file = data_dir + folder + '/tnet_new_' + str(times) + '.tnet'
		t.append(threading.Thread(target=run_tnet_new_multiple_times, args=(tree_file, out_file, times)))

	for i in range(len(t)):
		t[i].start()

	for i in range(len(t)):
		t[i].join()


# def compare_tnet_old_new(real_file, old_file, new_file):
# 	real = set(gr.get_real_edges(real_file))
# 	tnet_old = set(gr.get_mul_tnet_edges(old_file, 50))
# 	tnet_new = set(gr.get_mul_tnet_edges(new_file, 50))

# 	TP = len(real & tnet_old)
# 	FP = len(tnet_old - real)
# 	FN = len(real - tnet_old)
# 	print('Old TP', TP, 'FP', FP, 'FN', FN)

# 	TP = len(real & tnet_new)
# 	FP = len(tnet_new - real)
# 	FN = len(real - tnet_new)
# 	print('New TP', TP, 'FP', FP, 'FN', FN)
# 	print()

def create_favites_dataset():
	favites_data_main = '/data/Favites_data/'
	datasets = next(os.walk(favites_data_main))[1]
	# print(datasets)

	for dataset in datasets:
		cur_dir = favites_data_main + dataset
		folders = next(os.walk(cur_dir))[1]
		# print(folders)

		for folder in folders:
			net_file = cur_dir+ '/' +folder+ '/FAVITES_output/error_free_files/transmission_network.txt'
			rooted_tree = cur_dir+ '/' +folder+ '/RAxML_output/RAxML_rootedTree.'+ folder +'.rooted'
			new_dir = 'dataset/' +folder
			rooted_tree_copy = new_dir+ '/RAxML_rooted_tree.tree'
			net_copy = new_dir+ '/transmission_network.txt'

			if os.path.exists(rooted_tree) and os.path.exists(net_file):
				if not os.path.exists(new_dir):
					os.mkdir(new_dir)
				shutil.copy(rooted_tree, rooted_tree_copy)
				shutil.copy(net_file, net_copy)


def run_tnet_new_single(input_file):
	temp_out_file = 'output/single.temp'
	cmd = 'python3 tnet_print.py {} {}'.format(input_file, temp_out_file)
	os.system(cmd)
	# os.remove(temp_out_file)

def compare_tnets_directed(th = 50):
	data_dir = 'dataset/'
	folders = next(os.walk(data_dir))[1]
	folders.sort()

	TP_FP_FN_file = open('directed.tnet.old.new.th_'+ str(th) +'.TP_FP_FN.csv', 'w+')
	TP_FP_FN_file.write('dataset,tnet_old_tp,tnet_old_fp,tnet_old_fn,tnet_new_tp,tnet_new_fp,tnet_new_fn\n')
	F1_file = open('directed.tnet.old.new.th_'+ str(th) +'.F1.csv', 'w+')
	F1_file.write('dataset,tnet_old_prec,tnet_old_rec,tnet_old_f1,tnet_new_prec,tnet_new_rec,tnet_new_f1\n')

	for folder in folders:
		print('inside folder: ',folder)

		TP_FP_FN = []
		F1 = []

		real = set(ge.get_real_edges(data_dir + folder + '/transmission_network.txt'))
		tnet_old = set(ge.get_mul_tnet_edges(data_dir + folder + '/tnet_old_100.tnet', 50))
		tnet_new = set(ge.get_mul_tnet_edges(data_dir + folder + '/tnet_new_100.tnet', 50))

		TP = len(real & tnet_old)
		FP = len(tnet_old - real)
		FN = len(real - tnet_old)
		try:
			precision = TP/(TP+FP)
			recall = TP/(TP+FN)
			f1 = 2*(recall * precision) / (recall + precision)
		except ZeroDivisionError:
			precision = 0
			recall = 0
			f1 = 0

		TP_FP_FN.append(TP)
		TP_FP_FN.append(FP)
		TP_FP_FN.append(FN)
		F1.append(round(precision,3))
		F1.append(round(recall,3))
		F1.append(round(f1,3))

		TP = len(real & tnet_new)
		FP = len(tnet_new - real)
		FN = len(real - tnet_new)
		try:
			precision = TP/(TP+FP)
			recall = TP/(TP+FN)
			f1 = 2*(recall * precision) / (recall + precision)
		except ZeroDivisionError:
			precision = 0
			recall = 0
			f1 = 0

		TP_FP_FN.append(TP)
		TP_FP_FN.append(FP)
		TP_FP_FN.append(FN)
		F1.append(round(precision,3))
		F1.append(round(recall,3))
		F1.append(round(f1,3))

		TP_FP_FN_file.write('{},{},{},{},{},{},{}\n'.format(folder,TP_FP_FN[0],TP_FP_FN[1],TP_FP_FN[2],
							TP_FP_FN[3],TP_FP_FN[4],TP_FP_FN[5]))
		F1_file.write('{},{},{},{},{},{},{}\n'.format(folder,F1[0],F1[1],F1[2],F1[3],F1[4],F1[5]))

def main():
	# create_favites_dataset()
	# run_tnet_new_multithreaded()
	# run_tnet_old()
	compare_tnets_directed(50)



if __name__ == "__main__": main()
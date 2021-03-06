import bpy
import pickle
import os

print("File blender_scene.py called")

fp_data = open("gem_data.dat", 'rb')
fin = open("extracted_models.txt", 'r')
fnouns_id = open("nouns_and_IDs.txt", 'r')
fsent = open("Sentence.txt", 'r')
fout = open("Prep_nouns.txt", 'w') 

data = pickle.load(fp_data)

models = fin.read()
models = models.split(' ')
print(models)

line1 = fnouns_id.readline().split(" ")
nouns = list()
ids = list()
for j in range(len(models)-1):
	print(line1)
	nouns.append(line1[0])
	ids.append(line1[1])
	line1 = fnouns_id.readline().split(" ")
print("\n\n\n\n")
print(nouns)
print(ids)
print("\n\n\n\n")

placement_prepositions = {'right':['right'], 'up':['above', 'on', 'top'], 'left':['left'], 'down':['beneath', 'below', 'under']}
prepositions = ['right', 'left', 'up', 'down', 'above', 'below', 'on', 'beneath', 'top', 'front', 'back']

sentence = fsent.read().split(' ')
print(sentence)

prev_noun = ''
pres_noun = ''
last_prep = ''
prep_mapping = dict()
for n in range(len(sentence)):
	if sentence[n] in nouns:
		prev_noun = sentence[n]
		pres_noun = sentence[n]
		break
print(n)
# print(pres_noun)
# for p in range(n+1, len(sentence)):
# 	if sentence[p] in prepositions:
# 		# last_prep = sentence[p]
# 		# prep_mapping[last_prep].append([])
# 		print(prev_noun, sentence[p], end = ' ')
# 		fout.write(prev_noun + ' ' + sentence[p] + ' ')
# 	elif sentence[p] in nouns:
# 		print(sentence[p])
# 		fout.write(sentence[p] + '\n')
# 		prev_noun = sentence[p]
for p in range(n+1, len(sentence)):
	if sentence[p] in prepositions:
		for j in range(p+1, len(sentence)):
			if sentence[j] in nouns:
				print(sentence[j], sentence[p], prev_noun)
				fout.write(sentence[j] + ' ' + sentence[p] + ' ' + prev_noun + '\n')
				break
	elif sentence[p] in nouns:
		prev_noun = sentence[p]

fout.close()

# print(os.system("python3 modify_sentence_order.py"))

path = "/Volumes/My Passport/SHAPE/models-OBJ/models/"
path2 = "/Volumes/My Passport/SHAPE/Models/Volumes/My Passport/SHAPE/Models/"
x_dims_count = 0
y_dims_count = 0
z_dims_count = 0

x_dims_count_left = 0
y_dims_count_left = 0
z_dims_count_left = 0

fnouns_preps = open("Prep_nouns.txt", 'r')  # change
data1 = fnouns_preps.read()
data1 = data1.split('\n')

new_models = list()
placed_models = dict()
combined_models = list()
print("\n\n\n\n")
data1.pop()
print(data1)
for i in data1:
	line2 = i.split(' ')
	print(line2)

	if line2[1] == 'right':
		print("\n\n\n\nRIGHT PLACEMENT\n\n\n\n")
		id1 = ids[nouns.index(line2[0])]
		id1 = id1.strip()
		print("\n\nRecieved ID1 is\n\n")
		id2 = ids[nouns.index(line2[2])]
		id2 = id2.strip()
		print("\n\nRecieved ID2 is\n\n")
		full_id = 'wss.' + id1
		dims = data[full_id]['dims']
		# rotation_info = data[full_id]['up']
		# unit = float(data[full_id]['unit'][0])
		rotation_info = data[full_id]['up']
		unit = float(data[full_id]['unit'][0])
		x_rot = 0
		y_rot = 0
		z_rot = 0
		model_id = id1 + '.obj'
		mtl_id = id1 + '.mtl'
		model_path = path + model_id
		print('\n\n\n\n\n\n\n')
		path1 = "/Volumes/My\ Passport/SHAPE/models-OBJ/models/"
		# path2 = "/Volumes/My Passport/SHAPE/Models/Volumes/My Passport/SHAPE/Models/"
		print(os.system("cd " + path1 + '\n' + 'cp ' + model_id + ' /Volumes/My\ Passport/SHAPE/Models'))
		print(os.system("cd " + path1 + '\n' + 'cp ' + mtl_id + ' /Volumes/My\ Passport/SHAPE/Models'))
		# os.system("cd " + path1 + '\n' + 'open ' + model_id + '.obj')


		if id1 not in placed_models:
			imported_object = bpy.ops.import_scene.obj(filepath=model_path)
			print("Object", model_id, "imported")
			obj_object = bpy.context.selected_objects[0]
			obj_object.delta_scale = (unit, unit, unit)
			obj_object.rotation_euler = (x_rot, y_rot, z_rot)
			bpy.ops.object.origin_set(type = 'GEOMETRY_ORIGIN')
			obj_object.location = (0, 0, 1.1034)
			x_dims_count += (float(dims[0]))/200 
			y_dims_count += (float(dims[1]))/200 
			z_dims_count += (float(dims[2]))/200
			placed_models[id1] = (0, 0, 2)
		else:
			print("\n\nMODEL", id1, "ALREADY IMPORTED\n\n")
			x_dims_count = placed_models[id1][0] + (float(dims[0]))/200
			y_dims_count = placed_models[id1][1] + (float(dims[1]))/200
			z_dims_count = placed_models[id1][2] + (float(dims[2]))/200

		full_id = 'wss.' + id2
		dims = data[full_id]['dims']
		rotation_info = data[full_id]['up']
		unit = float(data[full_id]['unit'][0])
		x_rot = 0
		y_rot = 0
		z_rot = 0
		model_id = id2 + '.obj'
		model_path = path + model_id
		imported_object = bpy.ops.import_scene.obj(filepath=model_path)
		print("Object", model_id, "imported")
		obj_object = bpy.context.selected_objects[0] 
		obj_object.delta_scale = (unit, unit, unit)
		obj_object.rotation_euler = (x_rot, y_rot, z_rot)
		bpy.ops.object.origin_set(type = 'GEOMETRY_ORIGIN')
		x = x_dims_count + (float(dims[0]))/200
		obj_object.location = (x, 0, 1.1034)
		x_dims_count += (float(dims[0]))/100
		placed_models[id2] = (x, 0, 0)


	elif line2[1] == 'left':
		print("\n\n\n\nLEFT PLACEMENT\n\n\n\n")
		id1 = ids[nouns.index(line2[0])]
		id1 = id1.strip()
		print("\n\nReceived ID1 is", id1, "\n\n")
		print("\n\n\n\n\n\n", nouns.index(line2[2]), "\n\n\n\n")
		id2 = ids[nouns.index(line2[2])]
		id2 = id2.strip()
		print("\n\nRecieved ID2 is", id2, "\n\n")
		full_id = 'wss.' + id1
		dims = data[full_id]['dims']
		rotation_info = data[full_id]['up']
		unit = float(data[full_id]['unit'][0])
		x_rot = 0
		y_rot = 0
		z_rot = 0
		model_id = id1 + '.obj'
		model_path = path + model_id
		print(os.system("cd " + path1 + '\n' + 'cp ' + model_id + ' /Volumes/My\ Passport/SHAPE/Models'))
		print(os.system("cd " + path1 + '\n' + 'cp ' + mtl_id + ' /Volumes/My\ Passport/SHAPE/Models'))
		# os.system("cd " + path1 + '\n' + 'open ' + model_id + '.obj')


		if id1 not in placed_models:
			imported_object = bpy.ops.import_scene.obj(filepath=model_path)
			print("Object", model_id, "imported")
			obj_object = bpy.context.selected_objects[0]
			obj_object.delta_scale = (unit, unit, unit)
			obj_object.rotation_euler = (x_rot, y_rot, z_rot)
			bpy.ops.object.origin_set(type = 'GEOMETRY_ORIGIN')
			obj_object.location = (0, 0, 1.1034)
			x_dims_count += (float(dims[0]))/200 
			y_dims_count += (float(dims[1]))/200 
			z_dims_count += (float(dims[2]))/200
			placed_models[id1] = (0, 0, 0)
		else:
			print("\n\nMODEL", id1, "ALREADY IMPORTED\n\n")
			x_dims_count = placed_models[id1][0] + (float(dims[0]))/200
			y_dims_count = placed_models[id1][1] + (float(dims[1]))/200
			z_dims_count = placed_models[id1][2] + (float(dims[2]))/200

		full_id = 'wss.' + id2
		dims = data[full_id]['dims']
		rotation_info = data[full_id]['up']
		unit = float(data[full_id]['unit'][0])

		x_rot = 0
		y_rot = 0
		z_rot = 0
		model_id = id2 + '.obj'
		model_path = path + model_id
		imported_object = bpy.ops.import_scene.obj(filepath=model_path)
		print("Object", model_id, "imported")
		obj_object = bpy.context.selected_objects[0] 
		obj_object.delta_scale = (unit, unit, unit)
		obj_object.rotation_euler = (x_rot, y_rot, z_rot)
		bpy.ops.object.origin_set(type = 'GEOMETRY_ORIGIN')
		x = x_dims_count + (float(dims[0]))/200
		obj_object.location = (-1*x, 0, 1.1034)
		x_dims_count += (float(dims[0]))/100
		placed_models[id2] = (-1*x, 0, 0)

	elif (line2[1] == 'above') or (line2[1] == 'on'):
		print("COMMAND WENT TO ABOVE CONDITION")
		id1 = ids[nouns.index(line2[0])]
		id1 = id1.strip()
		id2 = ids[nouns.index(line2[2])]
		id2 = id2.strip()
		full_id = 'wss.' + id1
		dims = data[full_id]['dims']
		rotation_info = data[full_id]['up']
		unit = float(data[full_id]['unit'][0])
		x_rot = 0
		y_rot = 0
		z_rot = 0
		model_id = id1 + '.obj'
		mtl_id = id1 + '.mtl'
		model_id2 = id2 + '.obj'
		mtl_id2 = id2 + '.mtl'
		model_path = path + model_id
		print('\n\n\n\n\n\n\n')
		path1 = "/Volumes/My\ Passport/SHAPE/models-OBJ/models/"
		print(os.system("cd " + path1 + '\n' + 'cp ' + model_id + ' /Volumes/My\ Passport/SHAPE/Models'))
		print(os.system("cd " + path1 + '\n' + 'cp ' + mtl_id + ' /Volumes/My\ Passport/SHAPE/Models'))
		print(os.system("cd " + path1 + '\n' + 'cp ' + model_id2 + ' /Volumes/My\ Passport/SHAPE/Models'))
		print(os.system("cd " + path1 + '\n' + 'cp ' + mtl_id2 + ' /Volumes/My\ Passport/SHAPE/Models'))

		print("\n\n\n\nIDs being sent to run.py are", id1, "and", id2)
		os.system('echo "alias blender=/Applications/Blender/blender.app/Contents/MacOS/blender" >> ~/.profile' + '\n' + 'alias blender=/Applications/Blender/blender.app/Contents/MacOS/blender' + '\n' + 'cd Models '+'\n'+'blender -b blank.blend --python run.py ' + id1 +'.obj ' + id2 +'.obj')
		# blender -b blank.blend --python run.py " + 'id1 +'.obj ' + id2 +'.obj
		path2 = '/Volumes/My Passport/SHAPE/Models/'
		# model_path = path2 + 'placed_normalized_prep_' + id1 + '.obj' + 'placed_normalized_prep_' + id2 + '.obj'
		model_path = path2 + 'combined'+'placed_normalized_prep_modified_'+id1+'.obj'+'placed_normalized_prep_modified_'+id2+'.obj'
		filename = 'combined'+'placed_normalized_prep_modified_'+id1+'.obj'+'placed_normalized_prep_modified_'+id2

		imported_object = bpy.ops.import_scene.obj(filepath=model_path)
		# print(ids.index(id1 + '\n'))
		# ids[ids.index(id1 + '\n')] = filename + '\n'
		# print("\n\n",ids)
		# # print(nouns.index(filename+'\n'))
		# print("\n\n-------------",ids[nouns.index(line2[0])],"\n\n")
		# data['wss.'+filename] = dict()
		# data['wss.'+filename]['dims'] = data['wss.'+id1]['dims']
		# combined_models.append(id1)
		print("Combined Object Imported")
		obj_object = bpy.context.selected_objects[0]
		# obj_object.delta_scale = (unit, unit, unit)
		obj_object.rotation_euler = (0, 0, 2)
		bpy.ops.object.origin_set(type = 'GEOMETRY_ORIGIN')
		obj_object.location = (0, -2, 1.1034)
		placed_models[id1] = (0, -2, 0)
		placed_models[id2] = (0,-2,0)



print(placed_models)

fin.close()
fp_data.close()
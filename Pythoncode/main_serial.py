import numpy as np
from functions_hardsphere import *
from create_a_lot_of_particles import *

l = 5
inputs_nr = 4
inputs_pos = [np.array([0.,0.]), np.array([0.,1.]), np.array([1.,0.]), np.array([1.,1.])]
inputs_vel = [np.array([5,0]), np.array([0,0]), np.array([-5,0]), np.array([0,0])]
inputs_rad = 0.1*np.ones(4)
inputs_mass = 1*np.ones(4)
box = [[-l/2,l/2],[l/2,l/2],[l/2,-l/2],[-l/2,-l/2]]

input_pos_1, input_pos_2, input_pos_all, input_vel_1, input_vel_2, input_vel_all, name_box1, name_box2, name_box_all = create_particles(10,l)

#### initialise state and run collisions up to time T ####
#### throws up error due to lack of wall ####

T = 2
IS = initial_state([0,1,2,3], inputs_pos, inputs_vel, inputs_rad, inputs_mass)
L = -np.ones(len(IS)) # last collision time for each atom
simulation = []
heap = create_heap(IS, box)


t = 0
while t < T:
    print(t)
    # possible collision
    entry = heapq.heappop(heap)
    
    if not isinstance(entry[4],str):
        # checking if collision is valid event
        if entry[1] < L[entry[3].n]:
            pass
        elif entry[1] < L[entry[4].n]:
            pass
        else: # collision valid
            
            # updating last collision times
            L[entry[3].n] = entry[0]
            L[entry[4].n] = entry[0]
            
            # new particle pos and vel
            posi, veli, posj, velj = collision(entry)
            print(posi, veli, posj, velj)
            
            #save previous pos and vel
            simulation.append([entry[0], entry[3].n, entry[4].n, posi, posj, veli, velj])

            # update pos and vel
            entry[3].update(posi, veli)
            entry[4].update(posj, velj) # this will change all heap pos and vels
            # may not matter as they're no longer be valid?
            
            # update heap
            for i in IS:
                # collisions with first sphere
                dt = check_collision(i, entry[3])
                if dt != None:
                    heapq.heappush(heap, (dt + entry[0],entry[0],i.n,i, entry[3]))
                # collisions with second
                dt = check_collision(i, entry[4])
                if dt != None:
                    heapq.heappush(heap, (dt + entry[0],entry[0],i.n,i, entry[4]))
            
            #update heap with wall collissions
            dtw, w = wall_collisions(entry[3], box)
            if dtw != None:
                heapq.heappush(heap,(dtw + entry[0],entry[0],entry[3].n,entry[3],w))
            dtw, w = wall_collisions(entry[4], box)
            if dtw != None:
                heapq.heappush(heap,(dtw + entry[0],entry[0],entry[4].n,entry[4],w))
                    
            # update time counter
            t = entry[0]
    else:
        # checking if collision is valid event
        if entry[1] < L[entry[3].n]:
            pass
        else: # collision valid
            
            # updating last collision times
            L[entry[3].n] = entry[0]
            
            # new particle pos and vel
            posi, veli, posj, velj = collision(entry)
            print(posi, veli, posj, velj)
            
            #save previous pos and vel
            simulation.append([entry[0], entry[3].n, posi, veli, entry[4]])

            # update pos and vel
            entry[3].update(posi, veli)
            
            # update heap
            for i in IS:
                # collisions with first sphere
                dt = check_collision(i, entry[3])
                if dt != None:
                    heapq.heappush(heap, (dt + entry[0],entry[0],i.n, i, entry[3]))
            
            #update heap with wall collissions
            dtw, w = wall_collisions(entry[3], box)
            if dtw != None:
                heapq.heappush(heap,(dtw + entry[0],entry[0],entry[3].n,entry[3],w))
                
            # update time counter
            t = entry[0]

print(simulation)
simulate(simulation, box, T, 1000, [inputs_pos, inputs_vel,inputs_rad], name='animation_serial')

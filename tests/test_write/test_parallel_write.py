# import multiprocessing as mp
# import time
# from tests.test_write.test_regular_stack_writer import generate_random_data
# import os
# import tempfile
# import numpy as np
# from smecv_grid.grid import SMECV_Grid_v052
# from io_utils.write.regular_cube import NcRegGridStack
#
# stack_out = r"C:\Temp\parallel_nc\stack.nc"
#
# def test_write_points():
#     # test writing a small stack of global validation results point by point
#     # out_root = tempfile.mkdtemp()
#
#
#     index = np.array(['2000-01-01 to 2010-12-10',
#                       '2011-01-01 to 2018-12-10'])
#     z = index
#
#     land_grid = SMECV_Grid_v052('land')
#
#     img_writer = NcRegGridStack(dx=0.25, dy=0.25, z=z, z_name='period')
#
#     gpis, lons, lats, cells = land_grid.subgrid_from_cells(2244).get_grid_points()
#     data = generate_random_data(z=index, n_var=5, size=lons.size)
#     idx = '2000-01-01 to 2010-12-10'
#     data_dict = data[idx]
#     img_writer.write_point(lons, lats, z=np.array([idx]*lons.size), data=data_dict)
#
#     idx = '2011-01-01 to 2018-12-10'
#     data_dict = data[idx]
#     img_writer.write_point(lons, lats, z=np.array([idx]*lons.size), data=data_dict)
#
#     start = time.time()
#     os.makedirs(stack_out, exist_ok=True)
#     img_writer.store_stack(os.path.join(stack_out, 'stack.nc'))
#     os.makedirs(imgs_out, exist_ok=True)
#     img_writer.store_files(imgs_out)
#     end = time.time()
#     print('Writing file took {} seconds'.format(end - start))
#
#     assert os.path.isfile(os.path.join(stack_out, 'stack.nc'))
#     assert len(os.listdir(imgs_out)) == index.size
#
# def worker(arg, q):
#     '''stupidly simulates long running process'''
#     start = time.clock()
#     s = 'this is a test'
#     txt = s
#     for i in range(200000):
#         txt += s
#     done = time.clock() - start
#     with open(fn, 'rb') as f:
#         size = len(f.read())
#     res = 'Process' + str(arg), str(size), done
#     q.put(res)
#     return res
#
# def listener(q):
#     '''listens for messages on the q, writes to file. '''
#
#     with open(fn, 'w') as f:
#         while 1:
#             m = q.get()
#             if m == 'kill':
#                 break
#             f.write(str(m) + '\n')
#             f.flush()
#
# def main():
#     #must use Manager queue here, or will not work
#     manager = mp.Manager()
#     q = manager.Queue()
#     pool = mp.Pool(mp.cpu_count() + 2)
#
#     #put listener to work first
#     watcher = pool.apply_async(listener, (q,))
#
#     #fire off workers
#     jobs = []
#     for i in range(80):
#         job = pool.apply_async(worker, (i, q))
#         jobs.append(job)
#
#     # collect results from the workers through the pool result queue
#     for job in jobs:
#         job.get()
#
#     #now we are done, kill the listener
#     q.put('kill')
#     pool.close()
#     pool.join()
#
# if __name__ == "__main__":
#    main()
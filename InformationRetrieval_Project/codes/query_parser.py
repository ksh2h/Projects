from query_processor import *
from universal_query_parser import *
from recommender import *
import time

from multiprocessing.pool import ThreadPool
def parser(query):
    view = ''
    if len(query) == 0:
        flag=1
        view = 'none'
        result = {}
    else:
        result = {}
        #query_comp = query.split('::')
        parser_result = universal_parser( query )
        if parser_result[0] == 1 :
            [author, venue] = parser_result[1:]
            pool = ThreadPool(processes=2)
            reco_thread = pool.apply_async( author_recommend, ( author , "aaa")  )
            result_thread = pool.apply_async( metapathapc, (author, venue) )
            view = 'list'
            flag = 0
            return (result_thread.get(), flag, view, reco_thread.get())

        elif parser_result[0] == 2:
            [c_author, venue] = parser_result[1:]
            pool = ThreadPool(processes=2)
            reco_thread = pool.apply_async( author_recommend, (c_author, "aaa") )
            result_thread = pool.apply_async( aco_apc_metapath, (c_author, venue) )
            view = 'list'
            flag = 0
            return (result_thread.get(), flag, view, reco_thread.get() )

        elif parser_result[0] == 3:
            [venue, ty] = parser_result[1:]
            result = numberofPublications(venue, ty)
            view = 'graph'
            flag = 0
            return (result, flag, view, [])

        elif parser_result[0] == 4:
            [author, ty] = parser_result[1:]
            pool = ThreadPool(processes=2)
            reco_thread = pool.apply_async( author_recommend, (author, "aaa") )
            result_thread = pool.apply_async( metapathay, (author, ty) )
            view = 'graph'
            flag = 0
            return (result_thread.get(), flag, view, reco_thread.get())

        elif parser_result[0] == 5:
            [fy, ty] = parser_result[1:]
            result = papersinrange(fy, ty);
            view = 'graph'
            flag = 0
            return (result, flag, view, [])

        elif parser_result[0] == 6:
            [a, fy, ty] = parser_result[1:]
            pool = ThreadPool(processes=2)
            reco_thread = pool.apply_async( author_recommend, (a, "aaa") )
            result_thread = pool.apply_async( yearwisePublication, (a, fy, ty) )
            view = 'graph'
            flag = 0
            return (result_thread.get(), flag, view, reco_thread.get())

        elif parser_result[0] == 7:
            [author, fy, ty] = parser_result[1:]
            pool = ThreadPool(processes=2)
            reco_thread = pool.apply_async( author_recommend, (author, "aaa") )
            result_thread = pool.apply_async( yearwiseCitation, (author, fy, ty) )
            view = 'graph'
            flag = 0
            return (result_thread.get(), flag, view, reco_thread.get())

if __name__ == '__main__':
    st = time.time()
    (result, flag, view, rec_arr) = parser('author Rudolf Ahlswede & venue IEEE #')
    

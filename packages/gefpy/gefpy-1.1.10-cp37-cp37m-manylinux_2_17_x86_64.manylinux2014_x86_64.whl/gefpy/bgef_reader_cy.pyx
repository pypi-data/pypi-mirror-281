# -*- coding: utf-8 -*-
# distutils: language=c++
# cython: language_level=3, boundscheck=False
# cython: c_string_type=unicode, c_string_encoding=utf8
# Created by huangzhibo on 2022/01/01
"""
    Provides access to the bgef_reader interface.
    For reading common bin GEF.
"""

from .bgef_reader cimport *
import numpy as np
cimport numpy as np
import array
from numpy cimport ndarray, import_array, PyArray_DATA
from typing import List, Union,Tuple
from cython cimport view
from gefpy.bgef_reader_helper import SamplingPointKind

# EXP_DTYPE = np.dtype([
#     ('x', np.uint32),
#     ('y', np.uint32),
#     ('count', np.uint32),
# ])

import_array()

#define the waring string!
OLD_FORMAT_WARNING_STRING:str = "Warning:your source data file only has gene column," \
                        "but you specify return gene_names and gene ids which is invalid!" \
                        "so we will return an empty array which has same size with gene_names for" \
                        " the gene_ids"

class GroupedSamplingCoor(object):
    def __init__(
        self,
        sampling_left_coors: List[int],
        sampling_middle_coors: List[int],
        sampling_right_coors: List[int],
    ) -> None:
        self.sampling_left_coors = sampling_left_coors
        self.sampling_middle_coors = sampling_middle_coors
        self.sampling_right_coors = sampling_right_coors


class GroupedSamplingSize(object):
    def __init__(
        self,
        sampling_left_size: int,
        sampling_middle_size: int,
        sampling_right_size: int,
    ) -> None:
        self.sampling_left_size = sampling_left_size
        self.sampling_middle_size = sampling_middle_size
        self.sampling_right_size = sampling_right_size


def compute_sampling_level_size(level: int) -> int:
    return pow(3, level)


def compute_sampling_stride(level: int) -> int:
    return pow(3, level + 1)


def compute_sampling_left_remainder(level: int) -> int:
    sampling_size: int = compute_sampling_level_size(level)
    # sampling_stride: int = compute_sampling_stride(level)
    return sampling_size // 2


def compute_sampling_middle_remainder(level: int) -> int:
    sampling_size: int = compute_sampling_level_size(level)
    # sampling_stride: int = compute_sampling_stride(level)
    return sampling_size + sampling_size // 2


def compute_sampling_right_remainder(level: int) -> int:
    sampling_size: int = compute_sampling_level_size(level)
    # sampling_stride: int = compute_sampling_stride(level)
    return sampling_size * 2 + sampling_size // 2


def compute_sampling_size_1d(
    group_flag: bool = True,
    level: int = 3,
    left_value: int = None,
    block_size: int = None,
) -> Union[int, GroupedSamplingSize]:
    sampling_left_remainder: int = compute_sampling_left_remainder(level=level)
    sampling_middle_remainder: int = compute_sampling_middle_remainder(level=level)
    sampling_right_remainder: int = compute_sampling_right_remainder(level=level)
    sampling_stride: int = compute_sampling_stride(level=level)

    print(
        "left:{} middle:{} right:{} stride:{}".format(
            sampling_left_remainder,
            sampling_middle_remainder,
            sampling_right_remainder,
            sampling_stride,
        )
    )

    left_remainder: int = left_value % sampling_stride
    grouped_count = GroupedSamplingSize(0, 0, 0)

    if left_remainder <= sampling_left_remainder:
        sampling_left = left_value + sampling_left_remainder - left_remainder
    elif left_remainder <= sampling_middle_remainder:
        grouped_count.sampling_middle_size += 1
        grouped_count.sampling_right_size += 1
        sampling_left = (
            left_value + sampling_left_remainder - left_remainder + sampling_stride
        )
    elif left_remainder <= sampling_right_remainder:
        grouped_count.sampling_right_size += 1
        sampling_left = (
            left_value + sampling_left_remainder - left_remainder + sampling_stride
        )
    else:
        sampling_left = (
            left_value + sampling_left_remainder - left_remainder + sampling_stride
        )

    right_value: int = left_value + block_size
    if sampling_left > right_value:
        sampling_left = right_value
    sampling_steps: int = (right_value - sampling_left) // sampling_stride
    right_remainder: int = (right_value - sampling_left) % sampling_stride

    # last_possible_sampling_left = sampling_left + sampling_steps * sampling_stride
    diff_middle_and_left: int = sampling_middle_remainder - sampling_left_remainder
    diff_right_and_left: int = sampling_right_remainder - sampling_left_remainder

    if right_remainder >= diff_right_and_left:
        ++sampling_steps
    elif right_remainder >= diff_middle_and_left:
        grouped_count.sampling_left_size += 1
        grouped_count.sampling_middle_size += 1
    elif right_remainder > 0:
        grouped_count.sampling_left_size += 1

    grouped_count.sampling_left_size += sampling_steps
    grouped_count.sampling_middle_size += sampling_steps
    grouped_count.sampling_right_size += sampling_steps

    if group_flag:
        return grouped_count
    else:
        return (
            grouped_count.sampling_left_size
            + grouped_count.sampling_middle_size
            + grouped_count.sampling_right_size
        )


def compute_allocate_element_size(
    grouped_x_size: GroupedSamplingSize = None,
    grouped_y_size: GroupedSamplingSize = None,
    sampling_nine: bool = True,
) -> int:
    x_size: int = (
        grouped_x_size.sampling_left_size
        + grouped_x_size.sampling_middle_size
        + grouped_x_size.sampling_right_size
    )
    y_size: int = (
        grouped_y_size.sampling_left_size
        + grouped_y_size.sampling_middle_size
        + grouped_y_size.sampling_right_size
    )
    if sampling_nine:
        return x_size * y_size
    else:
        return (
            x_size * y_size
            - grouped_x_size.sampling_middle_size * grouped_y_size.sampling_middle_size
        )


cdef class BgefR:
    cdef BgefReader* bgef_instance # Hold a C++ instance which we're wrapping
    cdef unsigned int exp_len
    cdef unsigned int gene_num
    cdef bool get_geneid

    def __cinit__(self, filepath, bin_size, n_thread, get_geneid=False):
        self.bgef_instance = new BgefReader(filepath, bin_size, n_thread, False)
        self.exp_len = self.bgef_instance.getExpressionNum()
        self.gene_num = self.bgef_instance.getGeneNum()
        self.get_geneid = get_geneid
        

    def __init__(self, filepath, bin_size, n_thread, get_geneid=False):
        """
        A class for reading common bin GEF.

        :param filepath: Input bin GEF filepath.
        :param bin_size: Bin size.
        :param n_thread: number of thread
        """
        pass

    def __dealloc__(self):
        del self.bgef_instance

    def bgef_close(self):
        """
        Close the bgef.
        """
        self.bgef_instance.closeH5()

    def get_expression_num(self):
        """
        Get the number of expression.
        """
        return self.bgef_instance.getExpressionNum()
    
    def is_old_format(self) -> bool:
        """
        if true,the data is old format,missing the gene id column
        else,contain the gene id column
        """
        return self.bgef_instance.isOldFormat()

    def get_cell_num(self):
        """
        Get the number of cell.
        """
        return self.bgef_instance.getCellNum()

    def get_gene_num(self):
        """
        Get the number of gene.
        """
        return self.bgef_instance.getGeneNum()

    def get_gene_names(self):
        """
        Get an array of gene names.
        """
        # cdef view.array gene_names = view.array((self.bgef_instance.getGeneNum(),),
        #                                         itemsize=32 * sizeof(char), format='32s', allocate_buffer=True)
        cdef vector[string] gene_names
        gene_names.reserve(self.gene_num)
        self.bgef_instance.getGeneNameList(gene_names)
        cdef vector[string] gene_ids = self.bgef_instance.getGeneIds()
        if self.get_geneid:
            if not self.is_old_format():
                return np.asarray(gene_names), np.asarray(gene_ids)
            else:
                print(OLD_FORMAT_WARNING_STRING)
                return np.asarray(gene_names),np.zeros(self.gene_num,dtype="<U1")
        else:
            return np.asarray(gene_names)

    def get_cell_names(self):
        """
        Get an array of cell ids.
        """
        cdef unsigned long long int[::1] cell_names = np.empty(self.get_cell_num(), dtype=np.uint64)
        # cdef view.array gene_names = view.array((self.bgef_instance.getGeneNum(),),
        #                                    itemsize=32*sizeof(char), format='32s', allocate_buffer=True)
        self.bgef_instance.getCellNameList(&cell_names[0])
        return np.asarray(cell_names)

    def get_cell_names2(self, np.ndarray[np.ulonglong_t, ndim=1] cell_names):
        """
        Get an array of cell ids.

        :param cell_names:    cell names.
        """
        # cdef unsigned long long int[::1] cell_names = np.empty(self.get_cell_num(), dtype=np.uint64)
        # cdef view.array gene_names = view.array((self.bgef_instance.getGeneNum(),),
        #                                    itemsize=32*sizeof(char), format='32s', allocate_buffer=True)
        self.bgef_instance.getCellNameList(<unsigned long long int *>cell_names.data)
        # return np.asarray(cell_names)

    def get_gene_data(self):
        """
        Get gene data.
        :return: (gene_index, gene_names)
        """
        cdef unsigned int[::1] gene_index = np.empty(self.exp_len, dtype=np.uint32)
        cdef vector[string] gene_names = self.bgef_instance.getSparseMatrixIndicesOfGene(&gene_index[0])
        cdef vector[string] gene_ids = self.bgef_instance.getGeneIds()
        if self.get_geneid:
            if not self.is_old_format():
                return np.asarray(gene_index), np.asarray(gene_names), np.asarray(gene_ids)
            else:
                print(OLD_FORMAT_WARNING_STRING)
                return np.asarray(gene_index),np.asarray(gene_names),np.zeros(self.gene_num,dtype="<U1")
        else:
            return np.asarray(gene_index), np.asarray(gene_names)

    def get_expression(self):
        """
        Get the all expression from bgef.

        :return: exp
        """
        cdef view.array exp = view.array((self.exp_len,4),
                                         itemsize=4*sizeof(char), format='I', allocate_buffer=False)
        exp.data = <char*>self.bgef_instance.getExpression()
        # arr = np.asarray(exp, dtype=EXP_DTYPE)
        # arr.astype(EXP_DTYPE)
        return np.asarray(exp)

    def get_reduce_expression(self):
        """
        Get the reduce expression
        """
        cdef view.array exp = view.array((self.get_cell_num(),4),
                                         itemsize=4*sizeof(char), format='I', allocate_buffer=False)
        exp.data = <char*>self.bgef_instance.getReduceExpression()
        # arr = np.asarray(exp, dtype=EXP_DTYPE)
        # arr.astype(EXP_DTYPE)
        return np.asarray(exp)

    def get_sparse_matrix_indices(self):
        """
        Gets indices for building csr_matrix.

        Examples:
        from scipy import sparse
        sparse.csr_matrix((count, indices, indptr), shape=(cell_num, gene_num))

        :param indices:  CSR format index array of the matrix. Cell id array, the column indices, is the same size as count.
        :param indptr:   CSR format index pointer array of the matrix. indptr length = gene_num + 1 .
        :param count:    CSR format data array of the matrix. Expression count.
        :return: (indices, indptr, count)
        """
        cdef unsigned int[::1] indices = np.empty(self.exp_len, dtype=np.uint32)
        cdef unsigned int[::1] indptr = np.empty(self.gene_num + 1, dtype=np.uint32)
        cdef unsigned int[::1] count = np.empty(self.exp_len, dtype=np.uint32)
        self.bgef_instance.getSparseMatrixIndices(&indices[0], &indptr[0], &count[0])
        return np.asarray(indices), np.asarray(indptr), np.asarray(count)

    def get_sparse_matrix_indices2(self):
        """
        Gets indices for building csr_matrix.

        Examples:
        from scipy import sparse
        sparse.csr_matrix((count, cell_ind, gene_ind), shape=(cell_num, gene_num))

        :param cell_ind:  CSR format index array of the matrix. same size as count.
        :param gene_ind:  CSR format index array of the matrix. same size as count.
        :param count:     CSR format data array of the matrix. Expression count.
        :return: (cell_ind, gene_ind, count)
        """
        cdef unsigned int[::1] cell_ind = np.empty(self.exp_len, dtype=np.uint32)
        cdef unsigned int[::1] gene_ind = np.empty(self.exp_len, dtype=np.uint32)
        cdef unsigned int[::1] count = np.empty(self.exp_len, dtype=np.uint32)
        self.bgef_instance.getSparseMatrixIndices2(&cell_ind[0], &gene_ind[0], &count[0])
        return np.asarray(cell_ind), np.asarray(gene_ind), np.asarray(count)


    def get_exp_data(self):
        """
        Get sparse matrix indexes of expression data.
    
        :return: (uniq_cell, cell_index, count)
        """
        cdef unsigned int[::1] cell_index = np.empty(self.exp_len, dtype=np.uint32)
        cdef unsigned int[::1] count = np.empty(self.exp_len, dtype=np.uint32)
        cdef vector[unsigned long long] uniq_cell
        uniq_cell.reserve(self.exp_len)
        self.bgef_instance.getSparseMatrixIndicesOfExp(uniq_cell, &cell_index[0], &count[0])
        return np.asarray(uniq_cell), np.asarray(cell_index), np.asarray(count)

    # def get_sparse_matrix_indices_of_gene(self):
    #     """
    #     Get gene data.
    #     :return: (gene_index, gene_names)
    #     """
    #     cdef unsigned int[::1] gene_index = np.empty(self.bgef_instance.getExpressionNum(), dtype=np.uint32)
    #     cdef view.array gene_names = view.array((self.bgef_instance.getGeneNum(),),
    #                                        itemsize=32*sizeof(char), format='32s', allocate_buffer=True)
    #
    #     self.bgef_instance.getSparseMatrixIndicesOfGene(&gene_index[0], <char*>gene_names.data)
    #     return np.asarray(gene_index), np.asarray(gene_names)


    def read_whole_exp_matrix(self,
                              unsigned int offset_x,
                              unsigned int offset_y,
                              unsigned int rows,
                              unsigned int cols,
                              string & key,
                              np.ndarray[np.uint8_t, ndim=1] matrix):
        """
        Get wholeExp matrix.

        :param offset_x: The starting position on the x-axis to be read.
        :param offset_y: The starting position on the y-axis to be read.
        :param rows:     Number of rows to read.
        :param cols:     Number of cols to read.
        :param key: MIDcount or genecount.
        :param matrix: When the value is greater than 255, it will be set to 255.
        :return:
        """
        self.bgef_instance.readWholeExpMatrix(offset_x, offset_y, rows, cols, key, <unsigned char*>matrix.data)


    def read_whole_exp_matrix_all(self, str key):
        """
        Get wholeExp matrix.

        :param key: MIDcount or genecount.
        :return: 2D Matrix: When the value is greater than 255, it will be set to 255.
        """
        cdef np.ndarray[np.uint8_t, ndim = 2] matrix = np.empty(self.get_whole_exp_matrix_shape(), dtype=np.uint8)
        self.bgef_instance.readWholeExpMatrix(key, <unsigned char*>matrix.data)
        return matrix

    def get_whole_exp_matrix_shape(self) -> np.ndarray:
        """
        Get the shape of wholeExp matrix.
        :return: [rows, cols]
        """
        cdef view.array shape = view.array((2,), itemsize=sizeof(unsigned int), format="I", allocate_buffer=False)
        shape.data = <char *>self.bgef_instance.getWholeExpMatrixShape()
        return np.asarray(shape)


    def get_filtered_data(self, region, genelist):
        """
        Get the gene exp matrix.
        
        """
        cdef vector[unsigned int] cell_ind
        cdef vector[unsigned int] gene_ind
        cdef vector[unsigned int] count
        cdef vector[string] gene_names
        cdef vector[unsigned long long] uniq_cell
        cdef vector[string] gene_ids

        self.bgef_instance.getfiltereddata(region, genelist, gene_names, uniq_cell, cell_ind, gene_ind, count, gene_ids)
        if self.get_geneid:
            if not self.is_old_format():
                return np.asarray(uniq_cell), np.asarray(gene_names), np.asarray(count), np.asarray(cell_ind), np.asarray(gene_ind), np.asarray(gene_ids)
            else:
                print(OLD_FORMAT_WARNING_STRING)
                return np.asarray(uniq_cell), np.asarray(gene_names), np.asarray(count), np.asarray(cell_ind), np.asarray(gene_ind),np.zeros(self.gene_num,dtype="<U1")
        else:
            return np.asarray(uniq_cell), np.asarray(gene_names), np.asarray(count), np.asarray(cell_ind), np.asarray(gene_ind)

    def get_filtered_data_exon(self, region, genelist):
        """
        Get the gene exp matrix.
        
        """
        cdef vector[unsigned int] cell_ind
        cdef vector[unsigned int] gene_ind
        cdef vector[unsigned int] count
        cdef vector[unsigned int] exon
        cdef vector[string] gene_names
        cdef vector[unsigned long long] uniq_cell
        cdef vector[string] gene_ids

        self.bgef_instance.getfiltereddata_exon(region, genelist, gene_names, uniq_cell, cell_ind, gene_ind, count, exon, gene_ids)
        if self.get_geneid:
            if not self.is_old_format():
                return np.asarray(uniq_cell), np.asarray(gene_names), np.asarray(count), np.asarray(cell_ind), np.asarray(gene_ind), np.asarray(exon), np.asarray(gene_ids)
            else:
                print(OLD_FORMAT_WARNING_STRING)
                return np.asarray(uniq_cell), np.asarray(gene_names), np.asarray(count), np.asarray(cell_ind), np.asarray(gene_ind), np.asarray(exon), np.zeros(self.gene_num,dtype="<U1")
        else:
            return np.asarray(uniq_cell), np.asarray(gene_names), np.asarray(count), np.asarray(cell_ind), np.asarray(gene_ind), np.asarray(exon)

    def get_offset(self):
        """
        Get the offset in bgef.

        :return: [minx, miny]
        """
        cdef int offval[2]
        self.bgef_instance.getOffset(offval)
        return offval[0], offval[1]
	
    def get_exp_attr(self):
        """
        Get the bgef attr.
        
        :return: [minx, miny, maxx, maxy, maxexp, resolution]
        """
        cdef int offval[6]
        self.bgef_instance.getExpAttr(offval)
        return offval[0], offval[1], offval[2], offval[3], offval[4], offval[5]

    def is_Contain_Exon(self):
        return self.bgef_instance.isContainExon()

    #the coor is x1,x2 y1 y2    
    # def get_dnb_data_legacy(self, bfilter, btop, level, data_range):
    #     cdef unsigned int cols = data_range[1] - data_range[0]
    #     cdef unsigned int rows = data_range[3] - data_range[2]
    #     cdef vector[unsigned long long] index

    #     dt = np.dtype([('x', '<f4'), ('y', '<f4'), ('MIDcount', '<u4'), ('genecount', '<u4'), ('color', '<f4')])
    #     dnbdata = np.zeros(shape=(rows*cols,), dtype=dt)
    #     cdef void* data = PyArray_DATA(dnbdata)
    #     cdef unsigned int cnt = self.bgef_instance.getleveldnb(bfilter, btop, level, data_range[0], data_range[2], rows, cols, data, index)
    #     return np.resize(dnbdata, cnt), np.asarray(index)
    
    def get_dnb_data(self,
                        do_sampling:bool,
                        is_top_block:bool,
                        sampling_level:int,
                        x1:int,
                        y1:int,
                        block_size_x:int,
                        block_size_y:int,
                        point_kind:int=SamplingPointKind.left_top) -> Tuple[ndarray,ndarray]:
        level_dnb_result_dtype = np.dtype([('x', '<f4'), ('y', '<f4'), ('MIDcount', '<u4'), ('genecount', '<u4'), ('color', '<f4')])
        if do_sampling and sampling_level > 0:
            grouped_x_size:GroupedSamplingSize = compute_sampling_size_1d(
                group_flag=True,
                level=sampling_level,
                left_value=x1,
                block_size=block_size_x
            )
            grouped_y_size:GroupedSamplingSize = compute_sampling_size_1d(
                group_flag=True,
                level=sampling_level,
                left_value=y1,
                block_size=block_size_y
            )
            #sampling 9 datas
            if is_top_block:
                sampling_element_size = compute_allocate_element_size(
                    grouped_x_size=grouped_x_size,
                    grouped_y_size=grouped_y_size,
                    sampling_nine=True
                )
            else:
                #sampling 8 datas!
                sampling_element_size = compute_allocate_element_size(
                    grouped_x_size=grouped_x_size,
                    grouped_y_size=grouped_y_size,
                    sampling_nine=False
                )
        else:
            sampling_element_size = block_size_x * block_size_y

        print("Python allocate {} elements...".format(sampling_element_size))
        out_sampling_array = np.empty(
            shape=(sampling_element_size,),
            dtype=level_dnb_result_dtype
        )
    
        out_sampling_index_array = np.empty(
            shape=(sampling_element_size,),
            dtype=np.uint64
        )

        cdef void* out_sampling_ptr = PyArray_DATA(out_sampling_array)
        cdef void* out_sampling_index_ptr = PyArray_DATA(out_sampling_index_array)
        
        cdef uint32_t sampling_count = self.bgef_instance.getleveldnb(
            do_sampling,is_top_block,sampling_level,x1,y1,block_size_x,block_size_y,point_kind,out_sampling_ptr,out_sampling_index_ptr)
        #here will allocate new memory!
        return np.resize(out_sampling_array,sampling_count),np.resize(out_sampling_index_array,sampling_count)
        
    def get_gene_dnb_data(self, bfilter, btop, level, data_range, gene_list):
        cdef unsigned int cols = data_range[1] - data_range[0]
        cdef unsigned int rows = data_range[3] - data_range[2]

        cdef vector[unsigned long long] index
        # cdef vector[levelgenednb] dnbdata

        self.bgef_instance.GetGenesLevelDnb(bfilter, btop, level, data_range[0], data_range[2], data_range[1], data_range[3], index, gene_list)
        
        data_format="""f:x:
        f:y:
        I:midcnt:
        f:color:
        """
        cdef int lnum = self.bgef_instance.getGeneDnbNum()
        cdef view.array dnbdata
        if lnum != 0:
            dnbdata = view.array((lnum,), itemsize=sizeof(levelgenednb), format=data_format, allocate_buffer=False)
            dnbdata.data = <char*>self.bgef_instance.getGeneDnbData()
            return np.asarray(dnbdata), np.asarray(index)
        else:
            return np.array([]), np.array([])
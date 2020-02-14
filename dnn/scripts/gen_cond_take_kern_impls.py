#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import argparse
from gen_elemwise_utils import DTYPES

def main():
    parser = argparse.ArgumentParser(
        description='generate elemwise impl files',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('--type', type=str, choices=['cuda'],
                        default='cuda',
                        help='generate cuda cond take kernel file')
    parser.add_argument('output', help='output directory')
    args = parser.parse_args()

    if not os.path.isdir(args.output):
        os.makedirs(args.output)

    assert  args.type =='cuda'
    cpp_ext = 'cu'

    for dtype in DTYPES.keys():
        fname = '{}.{}'.format(dtype, cpp_ext)
        fname = os.path.join(args.output, fname)
        with open(fname, 'w') as fout:
            w = lambda s: print(s, file=fout)

            w('// generated by gen_cond_take_kern_impls.py')
            w('#include "../kern.inl"')
            w('')
            if dtype == 'dt_float16':
                    w('#if !MEGDNN_DISABLE_FLOAT16')
            w('namespace megdnn {')
            w('namespace cuda {')
            w('namespace cond_take {')
            w('')

            w('inst_genidx(::megdnn::dtype::{})'.format(DTYPES[dtype][0]))
            w('#undef inst_genidx')
            w('')
            w('inst_copy(::megdnn::dtype::{})'.format(DTYPES[dtype][0]))
            w('#undef inst_copy')
            w('#undef inst_copy_')

            w('')
            w('}  // cond_take')
            w('}  // cuda')
            w('}  // megdnn')
            if dtype == 'dt_float16':
                w('#endif')

            print('generated {}'.format(fname))

    os.utime(args.output)

if __name__ == '__main__':
    main()
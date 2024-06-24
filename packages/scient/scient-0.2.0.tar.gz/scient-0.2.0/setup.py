# -*- coding: utf-8 -*-
"""
Created on Tue Jan  3 20:36:58 2017

@author: a
"""
package='scient'#包名,需与文件夹名一致
version='0.2.0'
#buildpy 需要编译为.c的.py文件，需明确列出文件名，否则打包wheel时无法定位ext_modules
#buildpy=['elect/test.py']
buildpy=[
"scient/calc_expr.py",
"scient/process.py",
"scient/service.py",
"scient/algorithm/weight.py",
"scient/algorithm/binning.py",
"scient/algorithm/correlate.py",
"scient/algorithm/distance.py",
"scient/algorithm/entropy.py",
"scient/algorithm/gene.py",
"scient/algorithm/kdtree.py",
"scient/algorithm/linear_regression.py",
"scient/algorithm/metric.py",
"scient/algorithm/pca.py",
"scient/algorithm/similar.py",
"scient/algorithm/trie.py",
"scient/associate/apriori.py",
"scient/associate/rule_merge.py",
"scient/associate/sbar.py",
"scient/cluster/bestkmeans.py",
"scient/cluster/fourstep.py",
"scient/cluster/seqsim.py",
"scient/graph/louvain.py",
# "scient/image/assess.py",
"scient/image/edge.py",
"scient/image/feature.py",
"scient/image/friqa.py",
"scient/image/hash.py",
"scient/image/kernel.py",
"scient/image/process.py",
"scient/image/threshold.py",
"scient/language/cut.py",
"scient/language/document.py",
"scient/language/entity.py",
"scient/language/hash.py",
"scient/language/keyword.py",
"scient/language/longest_common.py",
"scient/language/process.py",
"scient/language/tagging.py",
"scient/language/tokenize.py",
"scient/language/topic.py",
"scient/language/vocab.py",
"scient/neuralnet/utils.py",
"scient/neuralnet/activate.py",
"scient/neuralnet/attention.py",
"scient/neuralnet/bert.py",
"scient/neuralnet/crf.py",
"scient/neuralnet/dataset.py",
"scient/neuralnet/dropout.py",
"scient/neuralnet/esim.py",
"scient/neuralnet/function.py",
"scient/neuralnet/glove.py",
"scient/neuralnet/hypernet.py",
"scient/neuralnet/lora.py",
"scient/neuralnet/loss.py",
"scient/neuralnet/lstm.py",
"scient/neuralnet/lstm_crf.py",
"scient/neuralnet/mask_linear.py",
"scient/neuralnet/optimize.py",
"scient/neuralnet/prepare.py",
"scient/neuralnet/resnet.py",
"scient/neuralnet/skip_gram.py",
"scient/neuralnet/train.py",
"scient/neuralnet/transformer.py",
"scient/timeseries/filter.py",
"scient/timeseries/outlier.py",
"scient/timeseries/segment.py"
    ]
#include 需要复制tar.gz包中的资源文件或文件夹，必须是tar.gz中包含的资源
#include=['elect/data','elect/pkgs/jieba/analyse/idf.txt','elect/pkgs']
include=['scient/data','scient/test']
#exclude 需要排除的文件或文件夹，
#exclude=['elect/apps','elect/guard.py','elect/data/brand.json','elect/pkgs']+[package+'/nltk/'+i for i in os.listdir(package+'/nltk') if i.endswith('.py') and i.startswith('__') and i not in ['__init__.py']]
import os
exclude=[]+sum([[os.path.join(dirpath,f) for f in filenames if f.startswith('__') and f.endswith('.py') and f not in ['__init__.py']] for dirpath,_,filenames in os.walk(package)],[])
#include和exclude同时存在的内容，会exclude



#setup
keywords = ()
description = ""
long_description = ""#如果有README.md，该项会被README.md内容覆盖
url = ""
author = ""
author_email = ""
license = "Licence"
platforms = "any"
install_requires = ['numpy>=1.24.0', 'scipy>=1.12.0']#,'torch>=2.2.0']
#%%以下内容不可修改
import os,io
import sys
from setuptools import setup

#路径分隔符统一
include=[i.replace('\\','/') for i in include]
exclude=[i.replace('\\','/') for i in exclude]
buildpy=[i.replace('\\','/') for i in buildpy]

#README.md
if os.path.exists('README.md'):
    with io.open('README.md',encoding='utf-8') as f:
        long_description = f.read()

#生成MANIFEST.in
with open('MANIFEST.in','w') as f:
    for i in include:
        if os.path.isdir(i):
            f.write('recursive-include %s *\n'%i)
        if os.path.isfile(i):
            f.write('include %s\n'%i)
    for i in exclude:
        if os.path.isdir(i):
            f.write('recursive-exclude %s *\n'%i)
        if os.path.isfile(i):
            f.write('exclude %s\n'%i)

ext_modules=[]
if sys.argv[1] in ('sdist'):
    import re
    from Cython.Build import cythonize
    
    for i in buildpy:
        #如果.c已存在,删除
        if os.path.exists(i.replace('.py','.c')):
            os.remove(i.replace('.py','.c'))
        #将build_py编译为.c
        ext_modules+=cythonize(i)
    #clear comment
    expr=re.compile(r'/\*.*?\*/',re.S) 
    for m in ext_modules:
        for s in m.sources:
            with open(s) as f:
                text=f.read()
            text=re.sub(expr,'',text)
            with open(s,'w') as f:
                f.write(text)
else:# sys.argv[1] in ('build','bdist','build_ext',None,'install','develop','bdist_egg','bdist_wheel','register','upload'):
    from setuptools import Extension
    for i in buildpy:
        ext_modules.append(Extension(i.replace('.py','').replace('/','.'),sources=[i.replace('.py','.c')]))

#py_modules排除exclude文件夹、include文件夹
py_modules=[(dirpath,[i for i in dirnames if os.path.join(dirpath,i).replace('\\','/') not in exclude
                     and os.path.join(dirpath,i).replace('\\','/') not in include],filenames)
           for dirpath, dirnames, filenames in os.walk(package) if dirpath.replace('\\','/') not in exclude
           and dirpath.replace('\\','/') not in include]
#py_modules所有py文件
py_modules=sum([[os.path.join(dirpath,i).replace('\\','/') for i in filenames if i.endswith('.py')]
               for dirpath, _, filenames in py_modules],[])
#py_modules排除exclude文件、include文件、buildpy文件
py_modules=[i for i in py_modules if i not in exclude+include+buildpy]

setup(
    name = package,
    version = version,
    keywords = keywords,
    description = description,  
    long_description = long_description,
    long_description_content_type="text/markdown",
    url = url,  
    author = author,
    author_email = author_email,
    license = license,
    platforms = platforms,
    install_requires = install_requires,
    #打包范围
    py_modules=[i.replace('.py','') for i in py_modules],
    ext_modules=ext_modules,
    #没有packages、include_package_data，不影响打包tar.gz，但是打包whl会缺少include
    packages=[i.replace('/','.') for i in include if os.path.isdir(i)],
    include_package_data = True,
    )

#删除MANIFEST.in、.c、.egg-info
if sys.argv[1] in ('sdist'):
    os.remove('MANIFEST.in')
    for m in ext_modules:
        for s in m.sources:
            os.remove(s)
    for i in os.listdir(package+'.egg-info'):
        os.remove(package+'.egg-info/'+i)
    os.rmdir(package+'.egg-info')

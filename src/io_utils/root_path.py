# -*- coding: utf-8 -*-
# Copyright (c) 2019, TU Wien, Department of Geodesy and Geoinformation (GEO).
# All rights reserved.

# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
# ARE DISCLAIMED. IN NO EVENT SHALL VIENNA UNIVERSITY OF TECHNOLOGY,
# DEPARTMENT OF GEODESY AND GEOINFORMATION BE LIABLE FOR ANY DIRECT, INDIRECT,
# INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
# LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA,
# OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF
# LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING
# NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE,
# EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

import os
import platform


if platform.system() == "Windows":
    c = 'C:\\'
    d = 'D:\\'
    h = 'H:\\'
    r = 'R:\\'
    p = 'P:\\'
    x = 'X:\\'
    u = 'U:\\'
    dw = 'D:\\'
    dr = 'E:\\'

elif platform.system() == "Mac":
    user = os.getenv('USER')
    path = '/shares/' + user
    c = '/users/' + user + '/'
    d = '/data/'
    h = path + '/home/'
    r = path + '/radar/'
    p = path + '/photo/'
    x = path + '/exchange/'
    u = path + '/users/'
    dw = '/data-write/'
    dr = '/data-read/'

else: # Linux
    user = os.getenv('USER')
    path = '/shares/' + user
    c = '/home/' + user + '/'
    d = '/data/'
    h = path + '/home/'
    r = path + '/radar/'
    p = path + '/photo/'
    x = path + '/exchange/'
    u = path + '/users/'
    dw = '/data-write/'
    dr = '/data-read/'

src_root = os.path.join(os.path.dirname(os.path.abspath(__file__)))

test_root = os.path.join(src_root, '..', '..', 'tests')
if not os.path.exists(test_root):
    test_root = None
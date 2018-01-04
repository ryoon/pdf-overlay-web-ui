# Copyright (c) 2017, 2018 Ryo ONODERA <ryo@tetera.org>
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions
# are met:
#
# 1. Redistributions of source code must retain the above copyright
#    notice, this list of conditions and the following disclaimer.
# 2. Redistributions in binary form must reproduce the above copyright
#    notice, this list of conditions and the following disclaimer in the
#    documentation and/or other materials provided with the distribution.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
# "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED
# TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR
# PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS
# BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
# CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
# SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
# INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
# CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
# ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.

from flask import Flask, render_template, json, request, send_file
app = Flask(__name__)

from pdfrw import PdfReader, PdfWriter, PageMerge

from datetime import datetime

import io
import subprocess
import urllib.parse
import flask

@app.route('/')
def main():
  return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload():
  uploadedFiles = request.files.getlist('upload_files')

  if len(uploadedFiles) != 2:
    return 'Must be 2 files.'

  if uploadedFiles[0].filename == 'stamp.pdf' and uploadedFiles[1].filename == 'stamp.pdf':
    return 'stamp.pdf must be 1 file.'


  if uploadedFiles[0].filename == 'stamp.pdf':
    stampFile = uploadedFiles[0].stream
    inFile = uploadedFiles[1].stream
  elif uploadedFiles[1].filename == 'stamp.pdf':
    inFile = uploadedFiles[0].stream
    stampFile = uploadedFiles[1].stream
  else:
    return 'stamp.pdf must be provided.'

  outputPdf = PageMerge().add(PdfReader(stampFile).pages[0])[0]
  inputPdf = PdfReader(inFile)
  for page in inputPdf.pages:
    PageMerge(page).add(outputPdf, prepend=False).render()

  nowDatetime = datetime.now()
  nowString = nowDatetime.strftime('%Y%m%d%H%M%S')
  sendFileName = nowString + '.pdf'
  sendFilePath = 'tmp/' + sendFileName
  
  PdfWriter(sendFilePath, trailer=inputPdf).write()

  fileObj = open(sendFilePath, 'rb')
  return send_file(io.BytesIO(fileObj.read()),
    as_attachment=True,
    attachment_filename=sendFileName,
    mimetype='application/pdf'
  )


if __name__ == "__main__":
  app.run()



pCmdCallback _cmd_cbList[255] = {NULL};

int8 cmd_registerCallback(uint8 cmd, pCmdCallback cb){
  if (_cmd_cbList[cmd] != NULL){
    return 1; 
  }
  _cmd_cbList[cmd] = cb;
  return 0; 
}

pCmdCallback cmd_getCallback(uint8 cmd){
  return _cmd_cbList[cmd];
}

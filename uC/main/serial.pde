
#define SERIAL_CHARBUF_SIZE 16
//#define SERIAL_START_FLAG 'A'
//#define SERIAL_END_FLAG 'Z'
//#define SERIAL_ESCAPE '!'

#define SERIAL_START_FLAG 0x55
#define SERIAL_END_FLAG 0xAA
#define SERIAL_ESCAPE 0x7F

uint8 _serial_charBuf[SERIAL_CHARBUF_SIZE] = {0};
uint8 _serial_charBuf_head = 0;
uint8 _serial_charBuf_len = 0;

//Small queue implementation
int8 queuePush(uint8 item) {
  if (_serial_charBuf_len <  SERIAL_CHARBUF_SIZE) {
    //Since we have space, let's find where to put the new item
    uint8 insertPos = _serial_charBuf_head + _serial_charBuf_len;
    insertPos %= SERIAL_CHARBUF_SIZE;
    _serial_charBuf[insertPos] = item;
    _serial_charBuf_len++;
    
    return 0;
  }
  return -1;
}

int8 queuePeek(uint8 *item) {
  if (item == NULL) {
   return -2; 
  }
  
  if (_serial_charBuf_len > 0) { 
    *item = _serial_charBuf[_serial_charBuf_head];
    return 0;   
  }
  return -1;
}

int8 queuePop(uint8 *item) {
  if (item == NULL){
    return -2; 
  }
  
  if (_serial_charBuf_len > 0) {
    *item = _serial_charBuf[_serial_charBuf_head];

    _serial_charBuf_head++;
    _serial_charBuf_head %= SERIAL_CHARBUF_SIZE;
    
    _serial_charBuf_len--;
    return 0;
  }
  return -1;
}

int8 queueFlush() {
  _serial_charBuf_len = 0;
  _serial_charBuf_head = 0;
  return 0;
}

int8 queueSeek(uint8 idx, uint8 *item) {
 if (idx < queueSize() && item != NULL) {
   //We'll translate from index from the head to index from 0
   idx = (_serial_charBuf_head + idx) % SERIAL_CHARBUF_SIZE;
   *item = _serial_charBuf[idx];
   return 0;
 }
  
 return -1; 
}

int8 queueSize() {
  return _serial_charBuf_len;
}

void queuePrint() {
  SerialUSB.print("Queue Len: ");
  SerialUSB.print(queueSize());
  SerialUSB.print(" Queue Head: ");
  SerialUSB.print(_serial_charBuf_head);
  SerialUSB.print(" BUF: ");
  for (uint8 i = 0; i < SERIAL_CHARBUF_SIZE; i ++) {
    SerialUSB.print((char)_serial_charBuf[i]);    
    SerialUSB.print(" ");
  }
  SerialUSB.print("\r\n");
}

int8 queueTest() {
  queueFlush();
  //Let's fill the queue a few items into the queue
  for (uint8 i = 0; i < SERIAL_CHARBUF_SIZE; i++) {
    queuePush(i);
  }

  queuePrint();
  
  //We'll test the wrapping around when pushing
  //We'll pop an item so that the head is now at 1 and the length is SIZE
  //We'll then push an item.  The expected behavior is that the first entry 
  //of the array will be the item we just pushed
  uint8 item;
  queuePop(&item);
  queuePrint();
  queuePush(0xFF);
  queuePrint();
  
  //Let's seek the last item
  queueSeek(SERIAL_CHARBUF_SIZE - 1, &item);
  SerialUSB.println("Last Seek:");
  SerialUSB.println(item,HEX);
  
  //Next we'll test the wrapping around when popping
  for (int i = 0; i < SERIAL_CHARBUF_SIZE - 1; i++) {
   uint8 i;
   queuePop(&i);
  }
  queuePrint();

  return 0;
}

//int8 validMessageTest() {
//  //Let start by setting the following:
//  //Buffer = 0x11 0x22 0x33 0xAA with a checksum of 0xEF
//  //Length = 5, head = 0
//  //This should be correct
//  _serial_charBuf[0] = 0x11;
//  _serial_charBuf[1] = 0x22;
//  _serial_charBuf[2] = 0x33;
//  _serial_charBuf[3] = 0xAA;
//  _serial_charBuf[4] = 0xEF;
//  _serial_charBuf_len = 5;
//  _serial_charBuf_head = 0;
//  SerialUSB.print("ValidMessageTest1 ");
//  SerialUSB.println(_serial_validateMessage() == 0);
//  //Now let's try something that should fail
//  //Buffer = 0x11 0x22 0x33 0xAA with a checksum of 0xAA
//  //Length = 5, head = 0
//  _serial_charBuf[4] = 0xAA;
//  SerialUSB.print("ValidMessageTest2 ");
//  SerialUSB.println(_serial_validateMessage() == -1);  
//  
//}



int8 _serial_validateMessage() {
  uint8 sum = 0;
  for (int i = 0; i < queueSize(); i++) {
    uint8 item = 0;
    if (queueSeek(i, &item) == 0) {
      sum += item;
    }
  }
  if (sum == 0xFF) {
    return 0;
  }
  return -1;
}

uint8 _serial_escaped = 0;
uint8 _serial_inCmd = 0;

void serial_periodic() {

  while (SerialUSB.available() > 0) {
    uint8 ch = SerialUSB.read();
    
//    SerialUSB.print(ch);
    if (_serial_escaped) {
      _serial_escaped = 0;
      queuePush(ch);
    }else{
      if (ch == SERIAL_ESCAPE && _serial_inCmd) {
        _serial_escaped = 1;
      }else if (ch == SERIAL_START_FLAG) {
        queueFlush();
        _serial_inCmd = 1;
      }else if (ch == SERIAL_END_FLAG && _serial_inCmd) {
        
        //Process what is in the queue
//        toggleLED();
        _serial_inCmd = 0;
        uint8 i = 0;
        if (_serial_validateMessage() == 0 && queuePeek(&i) == 0) {
//          Serial1.print("Received Command:");
//          Serial1.println(i);
          pCmdCallback foo = cmd_getCallback(i);
          foo(&(_serial_charBuf[1]));
        }
        
//        queuePrint(); 
      }else if(_serial_inCmd) {
        queuePush(ch);
      }
    }
  }
}



//int8 serialTxTest() {
//  uint8 test[] = "ABC!!123Z";
//  serial_tx(test,7); 
//  SerialUSB.println("");
//}

//This function will take in a buffer and length
//It will spit out a byte stuffed string with the start and end flags
int8 serial_tx(uint8 *buf, uint8 len) {
  uint8 checksum = 0;
  SerialUSB.write(SERIAL_START_FLAG);
  for (uint8 i = 0; i < len; i++) {
    if (buf[i] == SERIAL_START_FLAG || buf[i] == SERIAL_END_FLAG  || 
        buf[i] == SERIAL_ESCAPE) {
      SerialUSB.write(SERIAL_ESCAPE);
    }
    checksum += buf[i];
    SerialUSB.write(buf[i]);
  }
  checksum = ~checksum;
  if (checksum == SERIAL_START_FLAG || checksum == SERIAL_END_FLAG ||
      checksum == SERIAL_ESCAPE) {
    SerialUSB.write(SERIAL_ESCAPE);
  }
  SerialUSB.write(checksum);
  
  SerialUSB.write(SERIAL_END_FLAG);
  
  return 0;
}

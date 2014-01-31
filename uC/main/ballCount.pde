#define GREEN_PIN 8
#define RED_PIN 9

void ballCount_init() {
  pinMode(GREEN_PIN, INPUT);
  pinMode(RED_PIN, INPUT);  
  
  attachInterrupt(GREEN_PIN, ballCount_greenisr, RISING);
  attachInterrupt(RED_PIN, ballCount_redisr, RISING);  
}

uint8 greenBallPresent = 0;
uint8 redBallPresent = 0;

void ballCount_greenisr() {
  greenBallPresent = 1;
}

void ballCount_redisr() {
  redBallPresent = 1;  
}

void ballCount_periodic() {
  if (greenBallPresent == 1) {
    greenBallPresent = 0;
    uint8 buf[] = {0x0A, 0x01, 0x00}
    serial_tx(buf);
  }
  
  if (redBallPresent == 1) {
    redBallPresent = 0;
  }
}



/*
  Running process using Process class.

 This sketch demonstrate how to run linux processes
 using an Arduino Yún.

 created 5 Jun 2013
 by Cristian Maglie

 This example code is in the public domain.

 http://www.arduino.cc/en/Tutorial/Process

 */
#include <Process.h>
#include <SoftTimer.h>


#define SEG_A 2
#define SEG_B 3
#define SEG_C 4
#define SEG_D 5
#define SEG_E 6
#define SEG_F 7
#define SEG_G 8
#define SEG_H 9

#define COM1 10
#define COM2 11
#define COM3 12
#define COM4 13


unsigned char table[11][8] =
{
  {0, 0,  1,  1,  1,  1,  1,  1},     //0
  {0, 0,  0,  0,  0,  1,  1,  0},     //1
  {0, 1,  0,  1,  1,  0,  1,  1},     //2
  {0, 1,  0,  0,  1,  1,  1,  1},     //3
  {0, 1,  1,  0,  0,  1,  1,  0},     //4
  {0, 1,  1,  0,  1,  1,  0,  1},     //5
  {0, 1,  1,  1,  1,  1,  0,  1},     //6
  {0, 0,  0,  0,  0,  1,  1,  1},     //7
  {0, 1,  1,  1,  1,  1,  1,  1},     //8
  {0, 1,  1,  0,  1,  1,  1,  1},     //9
  {0, 1,  1,  1,  1,  0,  0,  1}      //10 = E
};


String input = "";
int error=0;
int hit = 0;

void displayFun(Task* me) { 
  displayChars(input);
}

void change(Task* me) {
  Process p;    // Create a process and call it "p"
  Serial.println("Starting process.");
  p.begin("/root//weather.py"); // Process that launch the "curl" command
  p.addParameter("d9e2928b027102742b6f134fb91aea73"); // Add the URL parameter to "curl"
  p.run();    // Run the process and wait for its termination
  Serial.println("Process done.");
  // Print arduino logo over the Serial
  // A process output can be read with the stream methods
  String str=readStringFromProcess(p);
  Serial.print(str);
  // Ensure the last bit of data is sent.
  Serial.flush();
  input = str;
  hit = hit +1;
  Serial.print("hit - ");
  Serial.println(hit);
}

Task changer(200000, change);
Task displayer(10,displayFun);


void setup() {
  pinMode(SEG_A,OUTPUT);    //设置为输出引脚
  pinMode(SEG_B,OUTPUT);
  pinMode(SEG_C,OUTPUT);
  pinMode(SEG_D,OUTPUT);
  pinMode(SEG_E,OUTPUT);
  pinMode(SEG_F,OUTPUT);
  pinMode(SEG_G,OUTPUT);
  pinMode(SEG_H,OUTPUT);

  pinMode(COM1,OUTPUT);
  pinMode(COM2,OUTPUT);
  pinMode(COM3,OUTPUT);
  pinMode(COM4,OUTPUT);

  
  
  // Initialize Serial
  Serial.begin(9600);

  // Wait until a Serial Monitor is connected.
  //while (!Serial);
  Serial.println("Starting Bridge.");
// Initialize Bridge
  Bridge.begin();
  Serial.println("Bridge started.");

  // run various example processes
  //runCurl();

  input="10";
  SoftTimer.add(&changer);
  SoftTimer.add(&displayer);
  Serial.println("Timer started.");
}







String readStringFromProcess(Process p) {
  String str="";
  while (p.available() > 0) {
    char c = p.read();
    str += c;
  }
  return str;
}

void displayChars(String chars){
  //TODO
  if(isDigit(chars.charAt(0))){
    displayDigit(chars.charAt(0)-48,3);
    delay(10);
    displayDigit(chars.charAt(1)-48,4);
    delay(10);
  }else{
    displayDigit(10,1);
  }
}


void displayDigit(int num,int com) {     //显示函数，com可选数值范围1-4，num可选数值范围0-9

  digitalWrite(SEG_A,LOW);      //去除余晖
  digitalWrite(SEG_B,LOW);
  digitalWrite(SEG_C,LOW);
  digitalWrite(SEG_D,LOW);
  digitalWrite(SEG_E,LOW);
  digitalWrite(SEG_F,LOW);
  digitalWrite(SEG_G,LOW);
  digitalWrite(SEG_H,LOW);

  switch(com)           //选通位选
  {
    case 1:
      digitalWrite(COM1,LOW);   //选择位1
      digitalWrite(COM2,HIGH);
      digitalWrite(COM3,HIGH);
      digitalWrite(COM4,HIGH);
      break;
    case 2:
      digitalWrite(COM1,HIGH);
      digitalWrite(COM2,LOW);   //选择位2
      digitalWrite(COM3,HIGH);
      digitalWrite(COM4,HIGH);
      break;
    case 3:
      digitalWrite(COM1,HIGH);
      digitalWrite(COM2,HIGH);
      digitalWrite(COM3,LOW);   //选择位3
      digitalWrite(COM4,HIGH);
      break;
    case 4:
      digitalWrite(COM1,HIGH);
      digitalWrite(COM2,HIGH);
      digitalWrite(COM3,HIGH);
      digitalWrite(COM4,LOW);   //选择位4
      break;
    default:break;
  }

  digitalWrite(SEG_A,table[num][7]);      //a查询码值表
  digitalWrite(SEG_B,table[num][6]);
  digitalWrite(SEG_C,table[num][5]);
  digitalWrite(SEG_D,table[num][4]);
  digitalWrite(SEG_E,table[num][3]);
  digitalWrite(SEG_F,table[num][2]);
  digitalWrite(SEG_G,table[num][1]);
  digitalWrite(SEG_H,table[num][0]);
}


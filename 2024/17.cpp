
#include <future>
#include <vector>
#include <iostream>
using namespace std;

class Computer {
  public:
    Computer(long a, long b, long c, vector<int> program)
        : mA(a), mB(b), mC(c), mProgram(program) {
          i = 0;
        }

    long getA() {
      return mA;
    }

    void setA(long a) {
      mA = a;
    }

    long getB() {
      return mB;
    }

    void setB(long b) {
      mB = b;
    }

    long getC() {
      return mC;
    }

    void setC(long c) {
      mC = c;
    }

    bool programAndLogEqual() {
      return mProgram == mLog;
    }

    void printLog() {
      for (int o: mLog) {
        cout << o << ",";
      }
      cout << "\n";
    }

    long getComboOperand(int operand) {
      switch (operand) {
        case 4:
          return mA;
        case 5:
          return mB;
        case 6:
          return  mC;
        default:
          return operand;
      }
    }

    void adv(int operand) {
      int denom = getComboOperand(operand);
      long newA = floor(mA / pow(2, denom));

      setA(newA);
    }

    void bxl(int operand) {
      setB(mB ^ operand);
    }

    void bst(int operand) {
      long comboOp = getComboOperand(operand);
      setB(comboOp % 8);
    }

    void jnz(int operand) {
      if (mA == 0) {
        return;
      }

      i = operand;
    }

    void bxc(int operand) {
      setB(mB ^ mC);
    }

    void out(int operand) {
      long comboOp = getComboOperand(operand);
      int mod8 = comboOp % 8;

      mLog.push_back(mod8);
    }

    void bdv(int operand) {
      long denom = getComboOperand(operand);
      long newB = floor(mA / pow(2, denom));

      setB(newB);
    }

    void cdv(int operand) {
      long denom = getComboOperand(operand);
      long newC = floor(mA / pow(2, denom));

      setC(newC);
    }

    void run(int opcode, int operand) {
      switch (opcode) {
        case 0:
          adv(operand);
          break;
        case 1:
          bxl(operand);
          break;
        case 2:
          bst(operand);
          break;
        case 3:
          return jnz(operand);
        case 4:
          bxc(operand);
          break;
        case 5:
          out(operand);
          break;
        case 6:
          bdv(operand);
          break;
        case 7:
          cdv(operand);
          break;
        default:
          i = mProgram.size() + 1;
          return;
      }

      i += 2;
    }

    void runProgram() {
      int lastI = -1;

      while (i < mProgram.size()) {
        if (lastI == i) {
          break;
        }

        lastI = i;

        int opcode = mProgram.at(i);
        int operand = mProgram.at(i+1);

        // cout << "HERE: " << opcode << "|" << operand << "\n";

        run(opcode, operand);
      }
    }


  private:
    long mA;
    long mB;
    long mC;
    int i;
    vector<int> mProgram;
    vector<int> mLog;

};

long test_run(long a, long b, long c, vector<int> program) {
  long testA = 9999999999;
  while (true) {
    a = testA;

    Computer computer = Computer(a, b, c, program);
    computer.runProgram();
    // computer.printLog();

    if (computer.programAndLogEqual()) {
      return testA;
    }
    // if (testA >= 10000000000 && testA % 10000000000 == 0) {
    if ((testA % 10000000) == 0) {
      cout << "Checked up to " << testA << "\n";
    }
    testA += 1;

  }
}

int main() {
  long a = 37283687;
  // long a = 2024;
  long b = 0;
  long c = 0;

  vector<int> program = {2,4,1,3,7,5,4,1,1,3,0,3,5,5,3,0};
  // vector<int> program = {0,3,5,4,3,0};

  Computer computer = Computer(a, b, c, program);
  computer.runProgram();
  computer.printLog();

  long registerA = test_run(a, b, c, program);
  cout << "Register A: " << registerA << "\n";
}
const fs = require("fs");

function print(...args) {
  console.log(...args);
}

// let fp = fetch("dec8Instructions.txt");
// console.log(fp);
const INSTRUCTIONS = fs.readFileSync("dec8Instructions.txt", "utf8").trim();
const MAP_FILE = fs.readFileSync("dec8Map.txt", "utf8").trim();
const MAP = createMap(MAP_FILE);

// console.log(INSTRUCTIONS);
// console.log(MAP_FILE);

function createMap(text) {
  let map = {};
  let arr = text.split("\n");
  // print(arr);
  for (let node of arr) {
    let [k, v] = node.split(" = ");
    // print(k, v);
    let [l, r] = v.replace("(", "").replace(")", "").split(", ");
    // print(l, r);

    map[k] = { L: l, R: r };
  }

  return map;
}

function getStartingNodes() {
  let startingNodesArr = [];

  for (let node of Object.keys(MAP)) {
    if (node.substring(2) === "A") {
      startingNodesArr.push(node);
    }
  }

  return startingNodesArr;
}

function checkAllNodesEndWithZ(nodeArr) {
  for (let node of nodeArr) {
    if (node.substring(2) !== "Z") {
      return false;
    }
  }

  return true;
}

function getNextNodes(currentNodes, instruction) {
  let nextNodesArr = [];
  for (let node of currentNodes) {
    let nextNode = MAP[node][instruction];
    nextNodesArr.push(nextNode);
  }

  return nextNodesArr;
}

const gcd = (a, b) => (a ? gcd(b % a, a) : b);
const lcm = (a, b) => (a * b) / gcd(a, b);

function part1() {
  currentNode = "AAA";
  endNode = "ZZZ";

  let step = 0;
  while (true) {
    let instruction = INSTRUCTIONS[step % INSTRUCTIONS.length];
    step++;

    let nextNode = MAP[currentNode][instruction];

    if (nextNode === endNode) {
      break;
    }

    currentNode = nextNode;
  }

  print(`It took ${step} steps to reach ZZZ`);
}

function part2() {
  let startingNodes = getStartingNodes(MAP);
  print(startingNodes);

  // let step = 0;
  // let currentNodes = startingNodes;
  // while (true) {
  //   if (checkAllNodesEndWithZ(currentNodes)) {
  //     break;
  //   }

  //   let instruction = INSTRUCTIONS[step % INSTRUCTIONS.length];
  //   step++;

  //   let nextNodes = getNextNodes(currentNodes, instruction);

  //   currentNodes = nextNodes;

  //   if (step % 100000000 === 0) {
  //     print(step, currentNodes);
  //   }
  // }

  let stepsArr = [];

  for (let node of startingNodes) {
    let step = 0;
    let currentNode = node;

    while (true) {
      let instruction = INSTRUCTIONS[step % INSTRUCTIONS.length];
      step++;

      let nextNode = MAP[currentNode][instruction];

      if (nextNode.substring(2) === "Z") {
        print(`It took ${step} steps for ${node} to reach ${nextNode}`);
        stepsArr.push(step);
        break;
      }

      currentNode = nextNode;
    }
  }
  print(stepsArr);

  let lcmOfSteps = stepsArr.reduce(lcm);
  print(`It took ${lcmOfSteps} steps to reach all nodes ending with Z`);
}

part1();
part2();

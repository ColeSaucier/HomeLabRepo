const fz = require('zigbee-herdsman-converters/converters/fromZigbee');
const exposes = require('zigbee-herdsman-converters/lib/exposes');
const e = exposes.presets;

module.exports = [
  {
    zigbeeModel: ['zb-example-c6'],
    model: 'zb-counter-sensor',
    vendor: 'esphome',
    description: 'Custom counter Sensor',
    fromZigbee: [fz.flow_measurement],
    toZigbee: [],
    exposes: [e.numeric('counter', exposes.access.STATE).withUnit('count').withDescription('Incremental Counter')],
  }
];

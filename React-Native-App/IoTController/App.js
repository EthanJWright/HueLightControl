import React from 'react';
import { StyleSheet, View, Text, Dimensions, TouchableOpacity} from 'react-native';
import { Picker, Button, Alert, Modal, Switch } from 'react-native';
const { width, height } = Dimensions.get('window');
import Swiper from 'react-native-swiper';
import Slider from 'react-native-slider';

import { scale, moderateScale, verticalScale} from './scaling';
import { ColorPicker, toHsv } from 'react-native-color-picker'
import rand_string from './rand_strings';

import Icon from 'react-native-vector-icons/Ionicons';

const hexRgb = require('hex-rgb');

var hue_report = {
  'hue' : {
    'bedroom' : false,
    'fan' : false
  }
}

function apiCall(json, callback){
  fetch('http://73.78.132.90:5000/', {
    method: 'POST',
    headers: {
      Accept: 'application/json',
      'Content-Type': 'application/json',
    },
    body: JSON.stringify(json),
  })
  .then(response => response.json())
    .then(responseJson => {
      if(responseJson.hue_result){
      hue_report.hue.bedroom = responseJson.hue_result.bedroom.action.on
      hue_report.hue.fan = responseJson.hue_result.fan.action.on
      console.log(hue_report.hue.bedroom);
      console.log(hue_report.hue.fan);
      callback(responseJson);
      return responseJson
      }
      else{
        return {'hue_result' : 'failed'}
      }
    })
  console.log('hit api');
}

var set_lights = {
  'on' : function(group, callback){
    apiCall({
      'hue' : {
        'group' : group,
        'on' : 'True',
        'brightness' : 100
      }
    }, callback)
  },
  'off' : function(group, callback){
    apiCall({
      'hue' : {
        'group' : group,
        'on' : 'False',
        'brightness' : 100
      }
    }, callback)
  }
}

function set_computer(color, on){
  rgb = hexRgb(color);
  rgb_array = [rgb.red, rgb.green, rgb.blue]
  var json = {
    'computer' : {
      'brightness' : 100,
      'rgb' : rgb_array,
      'on' : on
    }
  }
  apiCall(json);
}

function set_door(color, on){
  rgb = hexRgb(color);
  rgb_array = [rgb.red, rgb.green, rgb.blue]
  var json = {
    'door' : {
      'brightness' : 100,
      'rgb' : rgb_array,
      'on' : on
    }
  }
  apiCall(json);
}

function lightsOn(callback){
  set_lights.on('all', callback);
}
function lightsOff(callback){
  set_lights.off('all', callback);
}

function toggleSpecific(isOn, group, callback){
  var state = isOn ? 'on' : 'off';
  set_lights[state](group, callback);
}

function getCurrent(callback){
  json = {
      'hue' : { 'group' : 'all' }
    };
  fetch('http://73.78.132.90:5000/', {
    method: 'POST',
    headers: {
      Accept: 'application/json',
      'Content-Type': 'application/json',
    },
    body: JSON.stringify(json),
  })
  .then(response => response.json())
    .then(responseJson => {
      callback(responseJson);
    })
}

export default class App extends React.Component {
  constructor(props){
    super(props);
    this.state = {
      fan : false,
      bedroom : false,
      value: 0.2,
      user: '',
      modalVisible: false,
      computer_rgb : '#ffffff',
      door_rgb : '#ffffff'
    }
  }

  updateSwitches(responseJson){
    this.setState({
      fan: Boolean(responseJson.hue_result.fan.state.all_on),
      bedroom:Boolean(responseJson.hue_result.bedroom.state.all_on)
    })
  }

  getUpdate = () => {
   json = {'hue' : {'group' : 'all'}}
    fetch('http://73.78.132.90:5000/', {
      method: 'POST',
      headers: {
        Accept: 'application/json',
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(json),
    })
    .then(response => response.json())
      .then(responseJson => {
        if(responseJson.hue_result){
          console.log(responseJson.hue_result.fan.state.all_on)
          this.updateSwitches(responseJson);
        }
      })
    .catch(function(error){
      console.log('Woops the error was: ' + error.message);
    })
    console.log('hit api');
  }


  componentDidMount(){
    this.getUpdate();
  }

  openModal(){
    this.setState({modalVisible:true});
  }
  closeModal(color, location){
    if(location === 'computer'){
      this.setState({computer_rgb:color});
      set_computer(color, true)
      this.setState({modalVisible:false});
    }
  }if(location === 'door'){
      this.setState({door_rgb:color});
      set_door(color, true)
      this.setState({modalVisible:false});
  }

  toggleFan = (value) => {
    this.setState({fan:value});
    toggleSpecific(value, 'fan', (json) => this.updateSwitches(json));
  }
  toggleBedroom = (value) => {
    this.setState({bedroom:value});
    toggleSpecific(value, 'bedroom', (json) => this.updateSwitches(json));
  }


  render() {
    return (
    <Swiper style={styles.wrapper} showsButtons={false}>
      /* ---------------------  Start Living Room Remote ------------- */
      <View style={styles.container}>
          <View style={styles.box}>
              <Text style={styles.title}>Living Room Remote</Text>
              <View style={styles.buttonsContainer}>
              <Text style={styles.labelText}>Living Room Lights</Text>
              <Switch
                style={{ transform: [{ scaleX: 2 }, { scaleY: 2 }] }}
                onValueChange={this.toggleFan}
                value={this.state.fan}
              />
              <Text style={styles.labelText}> Bedroom Lights</Text>
              <Switch
                style={{ transform: [{ scaleX: 2 }, { scaleY: 2 }] }}
                onValueChange={this.toggleBedroom}
                value={this.state.bedroom}
              />
              </View>
              <View style={styles.buttonsContainer}>
              <TouchableOpacity style={styles.button}
                  onPress={this.getUpdate}
              >
              <Icon name="md-refresh" size={30} color="#FFFFFF" />
              </TouchableOpacity>
                  <TouchableOpacity style={styles.button}
                      onPress={() => {
                        lightsOn((json)=>console.log('here'));
                        this.setState({
                          'fan' : true,
                          'bedroom' : true
                        });
                      }} 
                  >
                  <Text style={styles.buttonText}>Lights On</Text>
                  </TouchableOpacity>
                  <TouchableOpacity style={styles.button}
                      onPress={() => {
                        lightsOff((json)=>console.log('here'));
                        this.setState({
                          'fan' : false,
                          'bedroom' : false
                        });
                      }}
                  >
                  <Text style={styles.buttonText}>Lights Off</Text>
                  </TouchableOpacity>
              </View>
          </View>
      </View>
      /* ---------------------  End Living Room Remote ------------- */
      /* ---------------------  Start Computer RGB Remote ------------- */
      <View style={styles.container}>
          <View style={styles.box}>
              <Text style={styles.title}>Computer RGB Remote</Text>
            <Modal
              visible={this.state.modalVisible}
              animationType={'slide'}
              onRequestClose={() => this.closeModal(null)}
              >
            <View style={styles.modalContainer}>
                  <ColorPicker
                    onColorSelected={color => this.closeModal(color, 'computer')}
                    style={{flex: 1}}
                  />
            </View>
          </Modal>
          <Text style={styles.labelText}>Select RGB Color: </Text>
              <View style={styles.rgbContainer}>
              <TouchableOpacity
                style={{
                    borderWidth:1,
                    borderColor:'rgba(0,0,0,0.2)',
                    alignItems:'center',
                    justifyContent:'center',
                    height:150,
                    width:150,
                    backgroundColor:this.state.computer_rgb,
                    borderRadius:100,
                  }}
              onPress={() => this.openModal()}
              >
              </TouchableOpacity>
              </View>
              <View style={styles.buttonsContainer}>
                  <TouchableOpacity style={styles.button}
                      onPress={() => set_computer(this.state.computer_rgb, true)}
                  >
                  <Text style={styles.buttonText}>Lights On</Text>
                  </TouchableOpacity>
                  <TouchableOpacity style={styles.button}
                      onPress={() => set_computer(this.state.computer_rgb, false)}
                  >
                  <Text style={styles.buttonText}>Lights Off</Text>
                  </TouchableOpacity>
              </View>

          </View>
      </View>
      /* ---------------------  End Computer RGB Remote ------------- */
      /* ---------------------  Start Door RGB Remote ------------- */
      <View style={styles.container}>
          <View style={styles.box}>
              <Text style={styles.title}>Door RGB Remote</Text>
            <Modal
              visible={this.state.modalVisible}
              animationType={'slide'}
              onRequestClose={() => this.closeModal(null)}
              >
            <View style={styles.modalContainer}>
                  <ColorPicker
                    onColorSelected={color => this.closeModal(color, 'door')}
                    style={{flex: 1}}
                  />
            </View>
          </Modal>
          <Text style={styles.labelText}>Select RGB Color: </Text>
              <View style={styles.rgbContainer}>
              <TouchableOpacity
                style={{
                    borderWidth:1,
                    borderColor:'rgba(0,0,0,0.2)',
                    alignItems:'center',
                    justifyContent:'center',
                    height:150,
                    width:150,
                    backgroundColor:this.state.door_rgb,
                    borderRadius:100,
                  }}
              onPress={() => this.openModal()}
              >
              </TouchableOpacity>
              </View>
              <View style={styles.buttonsContainer}>
                  <TouchableOpacity style={styles.button}
                      onPress={() => set_door(this.state.door_rgb, true)}
                  >
                  <Text style={styles.buttonText}>Lights On</Text>
                  </TouchableOpacity>
                  <TouchableOpacity style={styles.button}
                      onPress={() => set_door(this.state.door_rgb, false)}
                  >
                  <Text style={styles.buttonText}>Lights Off</Text>
                  </TouchableOpacity>
              </View>

          </View>
      </View>

      /* ---------------------  End Door RGB Remote ------------- */
    </Swiper>
    );
  }
}

const styles = StyleSheet.create({
  wrapper: {
  },
    container: {
        width: width,
        height: height,
        backgroundColor: '#E0E0E0',
        alignItems: 'center',
        justifyContent: 'center',
    },
    box: {
        width: moderateScale(300),
        height: verticalScale(450),
        backgroundColor: 'white',
        borderRadius: 10,
        padding: scale(10),
        shadowColor: 'black',
        shadowOpacity: 0.5,
        shadowRadius: 3,
        shadowOffset: {
            height: 0,
            width: 0
        },
        elevation: 2
    },
    title: {
        textAlign: 'center',
        fontSize: moderateScale(20, 0.4),
        fontWeight: 'bold',
        marginBottom: 10,
        color: 'black'
    },
    extra: {
        textAlign: 'center',
        fontSize: moderateScale(14),
        marginBottom: 10,
        color: 'black'
    },

    text: {
        fontSize: moderateScale(14),
        color: 'black'
    },
    buttonsContainer: {
        flex: 1,
        justifyContent: 'flex-end',
        alignItems: 'center'
    },
  slider: {
    borderRadius: 100,
    marginBottom: moderateScale(10),
    alignItems: 'center',
    justifyContent: 'center',
  },
    button: {
        width: moderateScale(150, 0.3),
        height: moderateScale(45, 0.3),
        borderRadius: 100,
        marginBottom: moderateScale(10),
        backgroundColor: '#41B6E6',
        alignItems: 'center',
        justifyContent: 'center',
    },
    buttonText: {
        fontWeight: 'bold',
        fontSize: moderateScale(14),
        color: 'white'
    },
  labelText:{    
    padding: 20,
    textAlign: 'center',
    fontWeight: 'bold',
    fontSize: moderateScale(14),
    color: 'black'
    },
  rgbContainer: {
        flex: 1,
        justifyContent: 'center',
        alignItems: 'center'
    },
  modalContainer: {
    flex: 1,
    justifyContent: 'center',
  },
  innerContainer: {
    alignItems: 'center',
  }
});


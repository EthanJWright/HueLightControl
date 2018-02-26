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
      console.log(responseJson);
      return responseJson;
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

function set_all(color, on){
  rgb = hexRgb(color);
  rgb_array = [rgb.red, rgb.green, rgb.blue]
  var json = {
    'computer' : {
      'brightness' : 100,
      'rgb' : rgb_array,
      'on' : on
    },
    'door' : {
      'brightness' : 100,
      'rgb' : rgb_array,
      'on' : on
    },
      'hue' : {
        'group' : 'all',
        'on' : on,
        'brightness' : 100,
        'rgb' : rgb_array
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
      modalVisibleDoor: false,
      modalVisibleComputer: false,
      modalVisibleAll: false,
      hitting: 'computer',
      computer_rgb : '#ffffff',
      door_rgb : '#ffffff',
      all_rgb : '#ffffff',
      home_string : 'temp'
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

 call_back = (value) => {
   console.log("HERE")
 }
 
 updateHome(responseJson){
   this.setState({
     home_string : responseJson.check_home
   })
 }

 check_home = () => {
  json = {
    'check_home' : true
  }
  apiCall(json, this.updateHome);
}


  componentDidMount(){
    this.getUpdate();
  }

  openModal(){
    this.setState({modalVisible:true});
  }
  closeModal(color, key){
    if(this.state.setting === 'computer'){
      this.setState({computer_rgb:color});
      set_computer(color, true);
      this.setState({modalVisibleComputer:false});
    }
    if(this.state.setting === 'door'){
        this.setState({door_rgb:color});
        set_door(color, true);
        this.setState({modalVisibleDoor:false});
    }if(this.state.setting === 'all'){
      this.setState({computer_rgb:color,door_rgb:color,all_rgb:color});
      set_all(color, true);
      this.setState({modalVisibleAll:false});
    }
    else{
        this.setState({modalVisibleDoor:false});
        this.setState({modalVisibleComputer:false});
    }
  }

  openAndSetModal = (value) => {
    this.setState({setting:value});
    if(value === 'computer'){
      this.setState({modalVisibleComputer:true});
    }if(value === 'door'){
      this.setState({modalVisibleDoor:true});
    }if(value === 'all'){
      this.setState({modalVisibleAll:true});
    }
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
      <View style={styles.container}>
          <View style={styles.box}>
              <Text style={styles.title}>Computer RGB Remote</Text>
            <Modal
              visible={this.state.modalVisibleComputer}
              animationType={'slide'}
              onRequestClose={() => this.closeModal(null)}
              >
            <View style={styles.modalContainer}>
                  <ColorPicker
                    defaultColor='#ffff00'
                    onColorSelected={color => this.closeModal(color)}
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
              onPress={() => this.openAndSetModal('computer')}
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
      <View style={styles.container}>
          <View style={styles.box}>
              <Text style={styles.title}>Door RGB Remote</Text>
            <Modal
              visible={this.state.modalVisibleDoor}
              animationType={'slide'}
              onRequestClose={() => this.closeModal(null)}
              >
            <View style={styles.modalContainer}>
                  <ColorPicker
                    defaultColor='#ffff00'
                    onColorSelected={color => this.closeModal(color)}
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
              onPress={() => this.openAndSetModal('door')}
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
      <View style={styles.container}>
          <View style={styles.box}>
              <Text style={styles.title}>All Home RGB Remote</Text>
            <Modal
              visible={this.state.modalVisibleAll}
              animationType={'slide'}
              onRequestClose={() => this.closeModal(null)}
              >
            <View style={styles.modalContainer}>
                  <ColorPicker
                    defaultColor='#ffff00'
                    onColorSelected={color => this.closeModal(color)}
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
                    backgroundColor:this.state.all_rgb,
                    borderRadius:100,
                  }}
              onPress={() => this.openAndSetModal('all')}
              >
              </TouchableOpacity>
              </View>
              <View style={styles.buttonsContainer}>
                  <TouchableOpacity style={styles.button}
                      onPress={() => set_all(this.state.all_rgb, true)}
                  >
                  <Text style={styles.buttonText}>Lights On</Text>
                  </TouchableOpacity>
                  <TouchableOpacity style={styles.button}
                      onPress={() => set_all(this.state.all_rgb, false)}
                  >
                  <Text style={styles.buttonText}>Lights Off</Text>
                  </TouchableOpacity>
              </View>

          </View>
      </View>
      <View style={styles.container}>
          <View style={styles.box}>
              <Text style={styles.title}>Who is Home?</Text>
              <Text style={styles.title}>{this.state.home_string}</Text>
              <View style={styles.buttonsContainer}>
                  <TouchableOpacity style={styles.button}
                      onPress={() => this.check_home}
                  >
                  <Text style={styles.buttonText}>Check</Text>
                  </TouchableOpacity>
              </View>
          </View>
      </View>
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


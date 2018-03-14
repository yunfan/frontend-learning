import {h, app} from 'hyperapp'

const state = {
  connected: false,
  messages: [],
  backend: "ws://127.0.0.1:5678/",
  conn: null
}

const actions = {
  connect_server: e => (state, actions) => {
    if(state.connected) return
    let ws = new WebSocket(state.backend)
    ws.onopen = actions.ws_open
    ws.onmessage = actions.ws_message
    ws.onclose = actions.ws_close
    return { connected: true, conn: ws }
  },

  input_press: e => (state, actions) => {
    console.log(e)
    if(!state.connected) return
    if(e.keyCode!=13) return
    console.log('got you')
    console.log(state)
    let target = document.getElementById('myinput')
    state.conn.send(target.value)
    target.value = ""
    return
  },

  ws_open: e => (state, actions) => {
    console.log("connected")
  },

  ws_message: e => (state, actions) => {
    console.log(e)
    let new_messages = state.messages.slice(-9)
    new_messages.push(e.data)
    console.log(new_messages)
    console.log(state)
    return { messages: new_messages }
  },

  ws_close: e => (state, actions) => {
    return { connected: false, conn: null }
  },
}

const view=(state, actions) =>
    <div id="container" class="flex-container">
      {state.connected ? (
          <div class="flex-item flex-container">
          <div id="messages" class="flex-item">
          {
            state.messages.map(m => <div class="msg">{m}</div>)
          }
          </div>
          <div id="userdata" class="flex-item">
            <input id="myinput" type="text" onkeypress={ actions.input_press }></input>
          </div>
          </div>) : (
            <button id="connect" class="flex-item" onclick={ actions.connect_server }>connect</button>
        )}
  </div>


const main = app(state, actions, view, document.body)

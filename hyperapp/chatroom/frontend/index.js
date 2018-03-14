import {h, app} from 'hyperapp'

const state = {
  connected: false,
  messages: [],
  backend: "ws://127.0.0.1:5678/",
  conn: null
}

const actions = {
  connect_server: e => (state, view) => {
    if(state.connected) return
    let ws = new WebSocket(state.backend)
    ws.onopen = e => actions.ws_open(e)
    ws.onmessage = e => actions.ws_message(e)
    ws.onclose = e => actions.ws_close(e)
    return { connected: true, conn: ws }
  },

  input_press: (e) => {
    if(!state.connected) return
    if(e.keyCode!=13) return
    let target = document.getElementById('myinput')
    state.ws.send(target.value)
    target.value = ""
    return
  },

  ws_open: (e) => {
    console.log("connected")
  },

  ws_message: (e) => {
    console.log(e)
    let new_messages = state.messages.slice(-9)
    new_messages.push(e.data)
    console.log(new_messages)
    return { messages: new_messages }
  },

  ws_close: (e) => {
    return { connected: false, conn: null }
  },
}

const view=(state, actions) =>
    <div id="container" class="flex-container">
      {state.connected ? (
          <div class="flex-item flex-container">
          <div id="messages" class="flex-item">
          {
            state.messages.map(() => <div class="msg">{m}</div>)
          }
          </div>
          <div id="userdata" class="flex-item">
            <input id="myinput" type="text" onKeyPress={ (e) => actions.input_press(e) }></input>
          </div>
          </div>) : (
            <button id="connect" class="flex-item" onclick={ e => actions.connect_server(e) }>connect</button>
        )}
  </div>


const main = app(state, actions, view, document.body)

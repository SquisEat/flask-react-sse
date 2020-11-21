import React from 'react';
import './App.css';
import axios from 'axios'
import ReactTable from 'react-table'
import 'react-table/react-table.css'
import eruda from 'eruda'

//const localhost="https://localhost:5001"
const localhost="https://48a7c694d6e4.ngrok.io";

const api = axios.create(
    {
        "baseURL": localhost,
        "withCredentials": true,
        //"mode": 'no-cors',
        "headers": {
            //'Access-Control-Allow-Credentials':'True',
            //'Access-Control-Allow-Origin': "http://localhost:3000/"
        }
    }
);

function initConsole(){
    let el = document.createElement('div');
    document.body.appendChild(el);

    eruda.init({
        container: el,
        tool: ['console', 'elements', 'network']
    });
}

class App extends React.Component {
constructor(){
    super()
      this.state = {
        data: []
      };
      this.columns = [{
          Header:'UserId',
          accessor:'userId'
      },
      {
          Header:'Id',
          accessor:'id'
      },
      {
          Header:'Name',
          accessor:'name'
      },
      {
          Header:'Address',
          accessor:'address'
    }];
      //login();
    this.eventSource = null;
  }

    login(){
        var bodyFormDate = new FormData();
        bodyFormDate.append('username', 'user3');
        bodyFormDate.append('password', 'password');
        api.post("/login", bodyFormDate).then((response) => {
            //if (response.data) {
                console.log("loggato");
                api.get("/").then(response=>{

                });
                this.eventSource=new EventSource(localhost+"/events?channel=supplierID_3",{withCredentials: true});
                this.eventSource.addEventListener("newOrder", e => {
                        console.log("data event", e.data)
                        //this.updateState(JSON.parse(e.data))
                        this.updateState(this.state.data.concat(JSON.parse(e.data)))
                    }
                );
            //}
            //return response
        });

    }

    logout(){
        this.eventSource.close();
        api.get("/logout");
    }

    componentDidUpdate(){
        console.log("update state", this.state.data);
    };

  componentDidMount() {
    //login();
      initConsole();
      /*this.eventSource.addEventListener("newOrder", e => {
              console.log("data event", e.data)
              //this.updateState(JSON.parse(e.data))
          this.updateState(this.state.data.concat(JSON.parse(e.data)))
          }
    );*/

  /*axios.get("http://localhost:5001/",
  {headers: {'Access-Control-Allow-Origin': '*'}
  })
      .then(
        (result) => {
          this.setState({
            isLoaded: true,
            data: result.data
          });
        },
        (error) => {
          this.setState({
            isLoaded: true,
            error
          });
        }
      )*/
  }
     updateState(newState) {
        console.log("Server side event received at",new Date());
        this.setState(Object.assign({}, { data: newState }));
         //this.state.data.push(newState);
      }
  render() {
    return (
    <>
     <ReactTable data={this.state.data} columns={this.columns}/>
        <button style={{backgroundColor: "blue", padding: "1rem 2rem", color:"white"}} onClick={()=>this.login()}> Login </button>
        <button style={{backgroundColor: "red", padding: "1rem 2rem", color:"white"}} onClick={()=>this.logout()} > Logout </button>
            </>
    )

      /*return(
          ""
      )*/
}
}
export default App;

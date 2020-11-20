import React from 'react';
import './App.css';
import axios from 'axios'
import ReactTable from 'react-table'
import 'react-table/react-table.css'

function login(){
    var bodyFormDate = new FormData();
    bodyFormDate.append('username', 'user3');
    bodyFormDate.append('password', 'password');
    axios.post("http://127.0.0.1:5001/login?next=/", bodyFormDate,
        {headers: { withCredentials: true}});
}

function logout(){
    axios.get("http://127.0.0.1:5001/logout");
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
    this.eventSource = new EventSource("http://127.0.0.1:5001/events?channel=supplierID_3");
  }

    componentDidUpdate(){
        console.log("update state", this.state.data);
    };

  componentDidMount() {
    //login();
      this.eventSource.addEventListener("newOrder", e => {
              console.log("data event", e.data)
              //this.updateState(JSON.parse(e.data))
          this.updateState(this.state.data.concat(JSON.parse(e.data)))
          }
    );

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
        <button style={{backgroundColor: "blue", padding: "1rem 2rem", color:"white"}} onClick={()=>login()}> Login </button>
        <button style={{backgroundColor: "red", padding: "1rem 2rem", color:"white"}} onClick={()=>logout()} > Logout </button>
            </>
    )

      /*return(
          ""
      )*/
}
}
export default App;

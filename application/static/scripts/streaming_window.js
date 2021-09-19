import React from 'react'
import ReactLoading from "react-loading"
import io from 'socket.io-client'
import '../stylesheets/center.css'

const brokenImageStyle = {
	width : "auto",
	height : "auto",
	maxWidth : '100%',
	resizeMode : "contain"
}

export default class StreamingWindow extends React.Component {

	constructor(props){
		super(props)
		this.state = {
			image:  undefined,
			error: 	undefined
		}
		this.socket = io('/video_feed', { forceNew: true, autoConnect: false })
		this.socket.on("message", (message) => {
  					console.log(message["data"])
			})
	}
 	
	componentDidMount(){
		console.log("connecting to server");
		try {
			this.socket.open();
			console.log("connected to server, testing")
	    	this.socket.emit('test', {'data' : 'server_test_successful'})
		} catch (err) {
			this.setState (
				this.state = {
					image:  undefined,
					error: 	true,
					message: err
				}
			)
			const errMessage = "error connecting to serve " + message
			console.error(errorMessage)
			alert(errorMessage)
		}
  	}



	render(){

		return (
			<div> {
				(true || this.state.error) ?
					<img src="/static/content/fatal_error.png" class="center" style={brokenImageStyle}/>
					: <ReactLoading type={"bars"} color={"white"}/>
			}
			</div>

		)
	}
}

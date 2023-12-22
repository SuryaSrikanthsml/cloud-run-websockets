import { Component, OnInit } from '@angular/core';
import { WsService } from './services/ws.service';

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.css']
})
export class AppComponent implements OnInit {
  constructor(
    private socketservice: WsService
  ) { }
  title = 'angular';
  recievedMessages = '';
  text = 'type here';
  room = 'A'; // Default value

  ngOnInit(): void {
    this.socketservice.getMessage().subscribe((message: any) => {
      this.recievedMessages = this.recievedMessages + ' -- ' + message.msg
    })
  }

  joinroom() {
    this.socketservice.sendMessage('join', { 'room': this.room, 'msg': this.text })
  }

  sendmsg() {
    this.socketservice.sendMessage('text', { 'room': this.room, 'msg': this.text })
  }

  leaveroom() {
    this.socketservice.sendMessage('left', { 'room': this.room })
  }
}

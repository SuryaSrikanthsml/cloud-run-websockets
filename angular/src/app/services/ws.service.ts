import { Injectable } from '@angular/core';
import { Socket } from 'ngx-socket-io';
import { map } from 'rxjs/operators';

@Injectable({
  providedIn: 'root'
})
export class WsService {

  constructor(private socket: Socket) { }


  // Helper functions
  sendMessage(event: any, message: any) {
    this.socket.emit(event, message);
  }

  getMessage() {
    return this.socket.fromEvent('message').pipe(map((data: any) => data));
  }
}

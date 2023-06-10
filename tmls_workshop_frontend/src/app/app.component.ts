import { Component, ViewChild } from '@angular/core';
import { MatPaginator } from '@angular/material/paginator';
import { BackendService } from './backend.service';
import { FormControl } from '@angular/forms';

export interface ClientProfile {
  'name': string,
  'age': string,
  'company_name': string,
  'gender': string,
  'person_2': string,
  'relationship': string,
  'net_worth': string,
  'postal_code': string,
  'city': string,
  'province': string,
  'street': string
}

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.css']
})
export class AppComponent {
  title = 'orlando-hackathon-frontend';
  toggle = false;
  backendService;
  dataSource: any[] = [];
  displayedColumns: string[] = ['name',
    'age',
    'gender',
    'person_2',
    'relationship',
    'net_worth',
    'postal_code',
    'city',
    'province',
    'street',
    'company_name'];
  textInputForGPT = new FormControl('');
  messages: Message[] = [{ user: "Client Service Advisor Bot", "message": "Hello, how may I help you?" }];

  constructor(backendService: BackendService) {
    this.backendService = backendService;
  }

  @ViewChild(MatPaginator, { static: true }) paginator: MatPaginator | any;

  refreshChat() {
    this.messages = [];
  }

  sendMessage() {
    if (this.textInputForGPT.value) {
      this.messages.push({ "user": "You", "message": this.textInputForGPT.value.trim() })
      this.backendService.chat(this.textInputForGPT.value.trim()).subscribe(data => {
        if (data["data"].length == 0) {
          this.messages.push({"user":"Client Service Advisor Bot", "message": "No data found."})
        } else {

          const data_processed = data["data"]
          this.dataSource = data_processed;

          this.messages.push({ "user":"Client Service Advisor Bot", "message": "Updated the table below" })
        }
      })
    }

  }

  // hideProspectiveClientList() {
  //   this.dataSource = [];
  // }
}

export interface Client {
  name: string,
  age: string,
  gender: string,
  person_2: string,
  relationship: string,
  net_worth: string,
  postal_code: string,
  city: string,
  province: string,
  street: string
}

export interface Message {
  user: string;
  message: string
}
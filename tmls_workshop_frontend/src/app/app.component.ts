import { Component, ViewChild } from '@angular/core';
import { MatPaginator } from '@angular/material/paginator';
import { MatTableDataSource } from '@angular/material/table';
import { BackendService } from './backend.service';
import { FormControl } from '@angular/forms';


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
    'street'];
  textInputForGPT = new FormControl('');
  messages: Message[] = [{ user: "LLM", "message": "Hello, how may I help you?" }];

  constructor(backendService: BackendService) {
    this.backendService = backendService;
  }

  @ViewChild(MatPaginator, { static: true }) paginator: MatPaginator | any;


  // getProspectiveClientList() {
  //   if (this.textInputForGPT.value != null) {
  //     if (this.textInputForGPT.value.trim().length > 0) {
  //       this.backendService.getProspectiveClientList(this.textInputForGPT.value.trim()).subscribe(data => {
  //         const data_processed = data["data"].slice(0, 5);
  //         this.dataSource = data_processed;
  //         this.dataSource.paginator = this.paginator;
  //       })
  //     }
  //   }
  // }

  refreshChat() {
    this.messages = [];
  }

  sendMessage() {
    if (this.textInputForGPT.value) {
      this.messages.push({ "user": "You", "message": this.textInputForGPT.value.trim() })
      this.backendService.chat(this.textInputForGPT.value.trim()).subscribe(data => {

        const data_processed = data["data"]
        this.dataSource = [data_processed];

        this.messages.push({ "user": "LLM", "message": "Updated the table with information about " + data_processed['name'] })
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
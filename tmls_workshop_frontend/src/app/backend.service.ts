import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class BackendService {

  constructor(private http: HttpClient) { }

  private apiUrl = 'http://127.0.0.1:8000'

  chat(textInputForGPT: string): Observable<any> {
    return this.http.post<any>(this.apiUrl + '/chat', { textInputForGPT: textInputForGPT });
  }


}

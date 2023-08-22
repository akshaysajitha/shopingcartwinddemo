import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class MyServiceService {
  private generatedCode: string = ''; // Initialize as an empty string

  constructor(private http: HttpClient) {
    this.generateCode(); // Generate the initial code
    this.startInterval(); // Start the interval to regenerate the code
  }

  private generateCode() {
    this.generatedCode = this.generateRandom6DigitNumber();
  }

  private startInterval() {
    setInterval(() => {
      this.generateCode();
    }, 30 * 60 * 1000); // 30 minutes in milliseconds
  }

  private generateRandom6DigitNumber(): string {
    return Math.floor(Math.random() * 900000) + 100000 + ''; // Convert to string
  }

  getData(): Observable<any> {
    return this.http.get<any>('http://127.0.0.1:8000/home/');
  }

  cartpost(pid: any, name: any, rate: any, shortdiscretion: any, imageurl: any, discretion: any, quantity: number): Observable<any> {
    const addcartapi = 'http://127.0.0.1:8000/home/cartitemadd';

    const requestData = {
      generatedCode: this.generatedCode, // Include the generated 6-digit code
      pid: pid,
      name: name,
      rate: rate,
      shortdiscretion: shortdiscretion,
      imageurl: imageurl,
      discretion: discretion,
      quantity: quantity || 1// Include the quantity in the request
    };
    return this.http.post<any>(addcartapi, requestData);
  }
  getcartdata():Observable<any>{
    return this.http.get<any>('http://127.0.0.1:8000/home/cartview');
  }
  postFormValues(data: any): Observable<any> {
    const url = 'http://127.0.0.1:8000/home/cartcomplete';
    data.generatedCode = this.generatedCode;
    return this.http.post(url,data);
  }
  getvieworderitem():Observable<any>{
    return this.http.get<any>('http://127.0.0.1:8000/home/vieworderitem');
  }

}

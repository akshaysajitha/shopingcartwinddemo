import { Component, OnInit } from '@angular/core';
import { MyServiceService } from 'src/app/my-service.service';
import { Router } from '@angular/router';

@Component({
  selector: 'app-welcome',
  templateUrl: './welcome.component.html',
  styleUrls: ['./welcome.component.css']
})
export class WelcomeComponent implements OnInit {
  productdata!: any[];
  cartItems: any[] = []; // Array to store items in the cart
  

  constructor(private myservice: MyServiceService, private router: Router) {}

  ngOnInit() {
    this.myservice.getData().subscribe(
      (response) => {
        this.productdata = response;
        console.log('check', this.productdata);
      }
    );
  }

  onButtonClick(){
    this.router.navigate(['/cart']);
  }
  

  addtocart(item: any) {
    const { pid, name, rate, shortdiscretion, imageurl, discretion, quantity } = item;
  
    this.myservice.cartpost(pid, name, rate, shortdiscretion, imageurl, discretion, quantity)
      .subscribe(
        (response) => {
          console.log('Item added to cart:', response);
          // You can handle the response or perform further actions here
        },
        (error) => {
          console.error('Error adding item to cart:', error);
        }
      );
      this.onButtonClick()
  }
  
}

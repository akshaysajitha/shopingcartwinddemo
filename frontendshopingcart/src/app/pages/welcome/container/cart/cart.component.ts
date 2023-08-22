import { Component, OnInit } from '@angular/core';
import { MyServiceService } from 'src/app/my-service.service';
import { Router } from '@angular/router';
@Component({
  selector: 'app-cart',
  templateUrl: './cart.component.html',
  styleUrls: ['./cart.component.css']
})
export class CartComponent implements OnInit {
  productdata!: any[];
  totalPriceSum: string = '';
  cartsum:string=''
  constructor(private myservice: MyServiceService, private router: Router) { }

  ngOnInit(): void {
    this.myservice.getcartdata().subscribe(
      (response) => {
        this.productdata = response.cart_items;
        this.totalPriceSum=response.total_price_sum;
        this.cartsum=response.carttotal;
        console.log('check data element', this.cartsum);
      }
    );
  }

  onButtonClickproduct(){
    this.router.navigate(['/welcome']);
  }

  addressform(total:string){
    console.log('product total pass',total)
    this.router.navigate(['header'])
  
  }
  orderitemview(){
    this.router.navigate(['OrderviewComponent'])
  }
 

}

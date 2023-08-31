import { Component, Input, OnInit } from '@angular/core';
import { MyServiceService } from 'src/app/my-service.service';
import { Router } from '@angular/router';
import { ActivatedRoute } from '@angular/router';
@Component({
  selector: 'app-orderview',
  templateUrl: './orderview.component.html',
  styleUrls: ['./orderview.component.css']
})
export class OrderviewComponent implements OnInit {
  productdata!: any[];
  constructor(private myservice: MyServiceService, private router: Router,private route: ActivatedRoute) { }

  ngOnInit(): void {
    this.route.queryParams.subscribe(params => {
      if (params.productdata) {
        this.productdata = JSON.parse(params.productdata);
        console.log('Product data from query parameter:', this.productdata);
      } else {
        this.myservice.getvieworderitem().subscribe(
          (response) => {
            this.productdata = response;
            console.log('Product data from getvieworderitem():', this.productdata);
          }
        );
      }
    });
  }
  
  onButtonClickproduct(){
    this.router.navigate(['/welcome']);
  }

}

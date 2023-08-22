import { Component, OnInit } from '@angular/core';
import { MyServiceService } from 'src/app/my-service.service';
import { Router } from '@angular/router';
@Component({
  selector: 'app-orderview',
  templateUrl: './orderview.component.html',
  styleUrls: ['./orderview.component.css']
})
export class OrderviewComponent implements OnInit {
  productdata!: any[];
  constructor(private myservice: MyServiceService, private router: Router) { }

  ngOnInit(): void {
    this.myservice.getvieworderitem().subscribe(
      (response) => {
        this.productdata = response;
        console.log('check', this.productdata);
      }
    );
  }
  
  onButtonClickproduct(){
    this.router.navigate(['/welcome']);
  }

}

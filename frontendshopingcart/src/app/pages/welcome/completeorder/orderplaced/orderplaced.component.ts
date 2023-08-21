import { Component, OnInit } from '@angular/core';
import { Router } from '@angular/router';
import { MyServiceService } from 'src/app/my-service.service';
@Component({
  selector: 'app-orderplaced',
  templateUrl: './orderplaced.component.html',
  styleUrls: ['./orderplaced.component.css']
})
export class OrderplacedComponent implements OnInit {

  constructor(private router:Router, private service:MyServiceService ) { }

  ngOnInit(): void {
  }
  

  gotowelcomepage(){
    this.router.navigate(['/welcome']);
  }

}

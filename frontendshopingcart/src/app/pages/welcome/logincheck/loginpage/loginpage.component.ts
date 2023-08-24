import { Component, OnInit } from '@angular/core';
import { MyServiceService } from 'src/app/my-service.service';
import { Router } from '@angular/router';
import { FormBuilder, FormGroup, Validators } from '@angular/forms';
@Component({
  selector: 'app-loginpage',
  templateUrl: './loginpage.component.html',
  styleUrls: ['./loginpage.component.css']
})
export class LoginpageComponent implements OnInit {
  validateForm!: FormGroup;
  productdata!: any[];
  constructor(private myservice: MyServiceService, private router: Router,private fb: FormBuilder) { }

  ngOnInit(): void {
    this.validateForm = this.fb.group({
      email:[null,[Validators.required]],
      number:[null,[Validators.required]],
      remember: [true]
    });
  }

  // form submit 
  submitForm(): void {
    if (this.validateForm.valid) {
      console.log('submit', this.validateForm.value);
      
      const formValue = this.validateForm.value;
    this.myservice.uservalidation(formValue).subscribe(
      response => {
        this.productdata = response; 
        console.log('email number check',this.productdata)
      })
      // this.router.navigate(['/orderplaced'])
     
    } else {
      Object.values(this.validateForm.controls).forEach(control => {
        if (control.invalid) {
          control.markAsDirty();
          control.updateValueAndValidity({ onlySelf: true });
        }
      });
    }
    
  }
    
  // form submit end

}

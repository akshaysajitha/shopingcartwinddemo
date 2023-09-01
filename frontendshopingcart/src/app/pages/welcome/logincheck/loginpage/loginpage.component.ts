import { Component, OnInit } from '@angular/core';
import { MyServiceService } from 'src/app/my-service.service';
import { Router } from '@angular/router';
import { FormBuilder, FormGroup, Validators } from '@angular/forms';
import { ActivatedRoute } from '@angular/router';
@Component({
  selector: 'app-loginpage',
  templateUrl: './loginpage.component.html',
  styleUrls: ['./loginpage.component.css']
})
export class LoginpageComponent implements OnInit {
  validateForm!: FormGroup;
  productdata!: any[];
  submittedNumber: number | null = null;
  constructor(private myservice: MyServiceService, private router: Router,private fb: FormBuilder,private route: ActivatedRoute) { }

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
      const formValue = this.validateForm.value;
      const submittedNumber = formValue.number;
  
      // Save the phone number in localStorage
      localStorage.setItem('userPhoneNumber', submittedNumber);
  
      // Continue with your API call
      this.myservice.uservalidation(formValue).subscribe(
        response => {
          this.productdata = response.cart_items;
          this.router.navigate(['/OrderviewComponent']);
  
          // Navigate to the orderview page with query parameters
          // this.router.navigate(['/OrderviewComponent'], { queryParams: { productdata: JSON.stringify(this.productdata) } });
        },
        error => {
          console.error('Error:', error);
        }
      );
    } else {
      Object.values(this.validateForm.controls).forEach(control => {
        if (control.invalid) {
          control.markAsDirty();
          control.updateValueAndValidity({ onlySelf: true });
        }
      });
    }
  }
  
  logout(){
    localStorage.clear();
  }
    
  // form submit end

}

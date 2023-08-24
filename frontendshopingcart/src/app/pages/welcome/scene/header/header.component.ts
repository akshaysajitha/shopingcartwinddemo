import { Component, OnInit } from '@angular/core';
import { MyServiceService } from 'src/app/my-service.service';
import { Router } from '@angular/router';
import { FormBuilder, FormGroup, Validators } from '@angular/forms';
@Component({
  selector: 'app-header',
  templateUrl: './header.component.html',
  styleUrls: ['./header.component.css']
})
export class HeaderComponent implements OnInit {
  validateForm!: FormGroup;

  // form submit 
  submitForm(): void {
    if (this.validateForm.valid) {
      console.log('submit', this.validateForm.value);
      
      const formValue = this.validateForm.value;
    this.myservice.postFormValues(formValue).subscribe(
      response => {
        console.log('Form data sent successfully:', response);
        
      })
      this.router.navigate(['/orderplaced'])
      
    } else {
      Object.values(this.validateForm.controls).forEach(control => {
        if (control.invalid) {
          control.markAsDirty();
          control.updateValueAndValidity({ onlySelf: true });
        }
      });
    }}
  // form submit end



  constructor(private myservice: MyServiceService, private router: Router,private fb: FormBuilder) { 
    
  }

  ngOnInit(): void {

    this.validateForm = this.fb.group({
      userName: [null, [Validators.required]],
      city: [null, [Validators.required]],
      state: [null, [Validators.required]],
      country: [null, [Validators.required]],
      pincode: [null, [Validators.required]],
      email:[null,[Validators.required]],
      number:[null,[Validators.required]],

      remember: [true]
    });
  }


  onButtonClickproduct(){
    this.router.navigate(['/welcome']);
  }


}

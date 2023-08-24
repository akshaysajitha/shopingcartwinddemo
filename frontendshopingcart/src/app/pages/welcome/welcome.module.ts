import { NgModule } from '@angular/core';

import { WelcomeRoutingModule } from './welcome-routing.module';

import { WelcomeComponent } from './welcome.component';
import { CartComponent } from './container/cart/cart.component';
import { HeaderComponent } from './scene/header/header.component';
import { CommonModule } from '@angular/common';
import { NzCardModule } from 'ng-zorro-antd/card';
import { NzIconModule } from 'ng-zorro-antd/icon';
import { NzButtonModule } from 'ng-zorro-antd/button';
import { NzDescriptionsModule } from 'ng-zorro-antd/descriptions';
import { FormsModule } from '@angular/forms'; 
import { NzFormModule } from 'ng-zorro-antd/form';
import { ReactiveFormsModule } from '@angular/forms';
import { OrderplacedComponent } from './completeorder/orderplaced/orderplaced.component';
import { NzResultModule } from 'ng-zorro-antd/result';
import { OrderviewComponent } from './orderitem/orderview/orderview.component';
import { LoginpageComponent } from './logincheck/loginpage/loginpage.component';
@NgModule({
  imports: [WelcomeRoutingModule,CommonModule,NzCardModule,NzIconModule,NzButtonModule,NzDescriptionsModule,
    FormsModule,NzFormModule,ReactiveFormsModule,NzResultModule],
  declarations: [WelcomeComponent, CartComponent, HeaderComponent, OrderplacedComponent, OrderviewComponent, LoginpageComponent],
  exports: [WelcomeComponent]
})
export class WelcomeModule { }

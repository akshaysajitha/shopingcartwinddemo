import { NgModule } from '@angular/core';

import { WelcomeRoutingModule } from './welcome-routing.module';

import { WelcomeComponent } from './welcome.component';
import { CartComponent } from './container/cart/cart.component';
import { HeaderComponent } from './scene/header/header.component';


@NgModule({
  imports: [WelcomeRoutingModule],
  declarations: [WelcomeComponent, CartComponent, HeaderComponent],
  exports: [WelcomeComponent]
})
export class WelcomeModule { }

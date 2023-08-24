import { NgModule } from '@angular/core';
import { Routes, RouterModule } from '@angular/router';
import { WelcomeComponent } from './welcome.component';
import { CartComponent } from './container/cart/cart.component';
import { OrderplacedComponent } from './completeorder/orderplaced/orderplaced.component';
import { OrderviewComponent } from './orderitem/orderview/orderview.component';
import { LoginpageComponent } from './logincheck/loginpage/loginpage.component';
const routes: Routes = [
  {path: '', component: WelcomeComponent },
  {path:'cart',component:CartComponent},
  {path:'orderplaced',component:OrderplacedComponent},
  {path:'OrderviewComponent',component:OrderviewComponent},
  {path:'login',component:LoginpageComponent}

];

@NgModule({
  imports: [RouterModule.forChild(routes)],
  exports: [RouterModule]
})
export class WelcomeRoutingModule { }

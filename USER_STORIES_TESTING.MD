# MediCart User stories testing documentation

This document outlines the testing procedures and results for each user story in the MediCart project. Each user story has been tested according to its acceptance criteria.

✅ = Passed | ❌ = Failed | 🟡 = Partially implemented | ⏳ = Not yet implemented

## Epic 1: User authentication & profile management

| User story             | Testing steps                                                                                                                                                   | Expected result                                                                                                                  | Status |
| ---------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------- | ------ |
| 1.1 User registration  | 1. Navigate to registration page<br>2. Enter email and password<br>3. Submit registration form<br>4. Check email for verification<br>5. Click verification link | - Form submits successfully<br>- Verification email received<br>- Account created after verification<br>- Welcome email received | ✅     |
| 1.2 User login         | 1. Navigate to login page<br>2. Enter credentials<br>3. Test password reset                                                                                     | - Successful login<br>- Password reset email received                                                                            | ✅     |
| 1.3 Profile management | 1. Access profile settings<br>2. Update personal information<br>3. Add shipping address<br>4. View order history                                                | - Information updates saved<br>- Order history displayed correctly                                                               | ✅     |

## Epic 2: Product management

| User story             | Testing steps                                                                                                       | Expected result                                                                                                          | Status |
| ---------------------- | ------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------ | ------ |
| 2.1 Product browsing   | 1. Browse product categories<br>2. Apply filters<br>3. Test sorting options<br>4. Use search function               | - Products display in grid<br>- Filters work correctly<br>- Sorting updates display<br>- Search returns relevant results | ✅     |
| 2.2 Product details    | 1. Click product card<br>2. View images and description<br>3. Check price and availability<br>4. Test "Add to Cart" | - Details page loads correctly<br>- Images display properly<br>- Product info is clear<br>- Add to cart works            | ✅     |
| 2.3 Product reviews    | 1. Submit product review<br>2. Rate product<br>3. View other reviews                                                | - Review submission works<br>- Star rating system functions<br>- Average ratings display on product cards                | ✅     |
| 2.4 Product comparison | 1. Select products to compare<br>2. View comparison table<br>3. Test sharing function                               | - Comparison table displays<br>- Features compared correctly<br>- Sharing works                                          | ⏳     |
| 2.5 Real-time search   | 1. Type in search box<br>2. Check dropdown results<br>3. Test on mobile devices                                     | - Results appear while typing<br>- Dropdown is responsive<br>- Works on all devices                                      | ⏳     |

## Epic 3: Shopping cart & checkout

| User story                   | Testing steps                                                                                                           | Expected result                                                                                                                 | Status |
| ---------------------------- | ----------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------- | ------ |
| 3.1 Shopping cart management | 1. Add items to cart<br>2. Update quantities<br>3. Remove items<br>4. Check cart persistence                            | - Items add/remove correctly<br>- Quantities update<br>- Totals calculate properly<br>- Cart saves between sessions             | ✅     |
| 3.2 Checkout process         | 1. Proceed to checkout<br>2. Select shipping address<br>3. Enter payment info<br>4. Complete purchase                   | - Checkout flow works<br>- Payment processes<br>- Order confirms<br>- Email received                                            | ✅     |
| 3.3 Guest checkout           | 1. Checkout as guest<br>2. Enter email<br>3. Complete purchase<br>4. Check order tracking                               | - Guest checkout works<br>- Order processes<br>- Tracking available<br>- Account creation offered                               | ✅     |
| 3.4 Wishlist                 | 1. Click heart icon on product<br>2. View wishlist page<br>3. Remove from wishlist<br>4. Check persistence after logout | - Items add/remove from wishlist<br>- Heart icon updates (red/grey)<br>- Wishlist persists for users<br>- Visual feedback shows | ✅     |

## Epic 4: Order management

| User story               | Testing steps                                                                                 | Expected result                                                               | Status |
| ------------------------ | --------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------- | ------ |
| 4.1 Order tracking       | 1. View order status<br>2. Check shipping updates<br>3. Test email notifications              | - Status updates show<br>- Shipping info accurate<br>- Notifications received | ⏳     |
| 4.2 Order history        | 1. View past orders<br>2. Download invoice<br>3. Test reorder function                        | - History displays correctly<br>- Invoices download<br>- Reorder works        | 🟡     |
| 4.3 Delivery preferences | 1. Set delivery preferences<br>2. Add special instructions<br>3. Update notification settings | - Preferences save<br>- Instructions recorded<br>- Notifications work         | ⏳     |

## Epic 5: Admin functionality

| User story             | Testing steps                                                                                                            | Expected result                                                                                                | Status |
| ---------------------- | ------------------------------------------------------------------------------------------------------------------------ | -------------------------------------------------------------------------------------------------------------- | ------ |
| 5.1 Product management | 1. Add new product<br>2. Edit existing product<br>3. Manage inventory                                                    | - Products add/edit<br>- Inventory updates<br>- Categories manage                                              | ✅     |
| 5.2 Order management   | 1. View orders<br>2. Update status<br>3. Search orders                                                                   | - Orders viewable<br>- Status updates<br>- Search works                                                        | ⏳     |
| 5.3 User management    | 1. Search users<br>2. Edit user roles<br>3. Manage accounts                                                              | - User search works<br>- Roles update<br>- Account management works                                            | ✅     |
| 5.4 Sales analytics    | 1. View dashboard<br>2. Generate reports<br>3. Export data                                                               | - Dashboard displays<br>- Reports generate<br>- Exports work                                                   | ⏳     |
| 5.5 Customer support   | 1. View customer details<br>2. Modify orders<br>3. Track issues                                                          | - Customer info accessible<br>- Order modifications work<br>- Issue tracking functions                         | ⏳     |
| 5.6 Customer request   | 1. Submit contact form<br>2. Check email confirmation<br>3. View in admin panel<br>4. Test auto-fill for logged-in users | - Form submits successfully<br>- Confirmation emails send<br>- Requests show in admin<br>- User info pre-fills | ✅     |

## Epic 6: Future features

| User story                  | Testing steps                                                                   | Expected result                                                        | Status |
| --------------------------- | ------------------------------------------------------------------------------- | ---------------------------------------------------------------------- | ------ |
| 6.1 Prescription management | 1. Upload prescription<br>2. Verify process<br>3. Check reminders               | - Upload works<br>- Verification process<br>- Reminders send           | ⏳     |
| 6.2 Live chat support       | 1. Start chat<br>2. Connect with staff<br>3. Rate session                       | - Chat connects<br>- Staff available<br>- Rating works                 | ⏳     |
| 6.3 Subscription service    | 1. Set up subscription<br>2. Test billing<br>3. Modify schedule                 | - Subscription creates<br>- Billing works<br>- Modifications save      | ⏳     |
| 6.4 Mobile app              | 1. Install app<br>2. Test features<br>3. Check notifications                    | - App functions<br>- Features work<br>- Notifications receive          | ⏳     |
| 6.5 AI recommendations      | 1. Create health profile<br>2. Check recommendations<br>3. Test personalization | - Profile creates<br>- Recommendations show<br>- Personalization works | ⏳     |

## Epic 7: User notifications

| User story                           | Testing steps                                                    | Expected result                                                           | Status |
| ------------------------------------ | ---------------------------------------------------------------- | ------------------------------------------------------------------------- | ------ |
| 7.1 Authentication notifications     | 1. Complete registration<br>2. Login/logout<br>3. Reset password | - Success messages show<br>- Login confirms<br>- Reset notifications work | ✅     |
| 7.2 Shopping cart notifications      | 1. Add to cart<br>2. Update quantity<br>3. Remove item           | - Add confirms<br>- Updates notify<br>- Removal confirms                  | ✅     |
| 7.3 Checkout notifications           | 1. Place order<br>2. Process payment<br>3. Complete checkout     | - Order confirms<br>- Payment notifies<br>- Completion confirms           | ✅     |
| 7.4 Product management notifications | 1. Add product<br>2. Update stock<br>3. Delete product           | - Addition confirms<br>- Stock alerts show<br>- Deletion confirms         | ✅     |
| 7.5 Error Notifications              | 1. Test form validation<br>2. Trigger payment error<br>          | - Validation shows<br>- Errors display                                    | ✅     |

## Legend

- ✅ = Passed: Feature is fully implemented and all tests pass
- ❌ = Failed: Feature is implemented but tests are failing
- 🟡 = Partially implemented: Feature is partially complete or under development
- ⏳ = Not yet implemented: Feature is planned but not yet implemented or tested

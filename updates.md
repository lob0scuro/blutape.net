# Updates - February 24, 2026

## Backend updates

- Fixed `get_current_status` flow and related machine status handling discussions/implementation.
- Normalized enum-related handling for machine fields to address DB insertion issues (including vendor-related length/value normalization work).
- Fixed export endpoint failures in `server/app/api/export.py`:
  - Replaced legacy query usage that caused `User.query` errors.
  - Updated report-building logic to align with current model structure.
  - Restored expected report payload structure for template/export rendering.
- Re-enabled export blueprint registration in API initialization so export routes are active.
- Added self-profile update support in backend update routes:
  - Added route/logic for users to update their own profile fields (non-password fields).
  - Preserved admin ability to update their own profile as well.

## Frontend updates

- Refactored and stabilized machine card flows in `client/src/routes/machines/card/Card.jsx` and related API helpers.
- Consolidated fetch/error handling patterns by introducing shared request utility:
  - Added `client/src/utils/api.js` (`requestJson`) and migrated multiple pages/components to it.
- Cleaned up imports and removed dead/unused code across multiple route components.
- Modularized machine route code into clearer API/helpers where applicable.
- Updated machines table route and control flow, including filtering/pagination cleanup.
- Reviewed and improved `Search.jsx` and admin route structure as requested.
- Added profile page and route wiring for logged-in users:
  - `client/src/routes/profile/Profile.jsx`
  - `client/src/routes/profile/Profile.module.css`
  - Route registration in app routing.

## Admin/permissions updates

- Updated `client/src/layout/AdminRoutes.jsx` permissions:
  - Metrics access is now admin-only.
  - Admin register-related protection maintained as admin-only.
- Kept role-aware navbar behavior for admin vs technician paths.

## Metrics page and export UX

- Refactored `client/src/routes/admin/Metrics.jsx` layout and data handling.
- Removed old green events background and adjusted metrics visual structure.
- Moved export controls to top area and showed controls conditionally when user is selected.
- Converted export control text to icon-friendly button behavior and iterated spacing/sizing/styling.
- Made events container scrollable to prevent overlong page stretch.
- Fixed CSV/PDF export click failures end-to-end after backend adjustments.

## Removed obsolete admin export/print files

- Removed:
  - `client/src/routes/admin/prints/UserMetricsPrintPage.jsx`
  - `client/src/routes/admin/prints/UserMetricsPrintPage.module.css`
  - `client/src/routes/admin/export/Export.jsx`
  - `client/src/routes/admin/export/Export.module.css`
- Removed associated route/import references.

## Mobile-first UI tuning

- Modernized floating bottom navbar styling for mobile-first usage.
- Tuned spacing/visual polish to better fit field usage patterns (mostly mobile users).
- Refactored machine table controls into a cleaner unified control panel:
  - User filter, status selector, and pagination now share a cohesive card layout.
  - Updated control styling for consistency and better small-screen readability.
- Converted `StatusBar` behavior toward select-based status control for smaller screens and refined integration styling.

## Quality checks

- Ran frontend linting after major UI refactors and cleanup.
- Resolved lint issues encountered during refactors (including hook and config-related warnings/errors where applicable).

## Current state

- Admin metrics/export flow is functioning.
- Metrics access control is admin-only.
- User self-profile updates (excluding password changes) are in place.
- Machines control section has been refactored into a cleaner mobile-first layout.
- Additional DB migration planning from legacy `server/app/models.py` to modular `server/app/models/*` is documented for follow-up tomorrow.

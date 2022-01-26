# Fetching Reports

### Purpose

We had a custom integration with a shipper, and the packages that would go out via UPS had to be tracked separately. As part of this process, we wanted to automate archiving the invoice-manifest combo they sent to us on every Sunday.

From there, we looked at making some reports based on these figures.

### Boilerplate

`Pipfile` shows that `pycurl`, `pysftp`, and `pandas` are requirements. Strictly speaking, pandas is only required for some of the extra reports, so in the future, I should probably put that as a dev requirement for myself until the report modification scripts are integrated.

`.env` contains credentials for the SFTP account given by our shipper.

`startenv.sh` was a stopgap to run the script via `cron`. This was deprecated upon creating `ups_fetch.service` and `ups_fetch.timer` and integrating them into SystemD.

`header_master.txt` is a reference file of all the headers available and in what order based on our provider.

`headers.py` is a list of headers, in order, as they appear in our report, with comments filling in where the others would be if they were to be included. This ended up being mostly reference early on in the process of understanding reporting.

### get_ups_files.py

Script to auomatically grab the most recent report (as there were sometimes two or three past ones there) via SFTP. The provider's timestamps were not reliable and so we had to parse filenames for dates. Fairly straightforward.

### monthly_breakdown.py

This was our primary breakdown. Our provider would provide each separate charge for a given order on a new line item.

>Not actually our data and formatting, but the basics are here in this example:
>
>name, address, distributor, charge, charge type, ...
>john smith, 233 1st St., Jabra, 1.02, base charge, ...
>john smith, 233 1st St., Jabra, 4.31, distance charge, ...
>john smith, 233 1st St., Jabra, 9.16, dimensional weight charge, ...
>jane wright, 73 43rd Ave., Apple, 3.76, actual weight charge, ...
>jane wright, 73 43rd Ave., Apple, 1.02, base charge, ...

We summed all charges for a given order, and also made note of the Weight Code used by the provider in order to determine the actual shipping.

These reports were used by Logisitics to determine how our free shipping pilot fared vs. our prices.

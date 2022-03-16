import enum
import subprocess
from django.db import models
from django.conf import settings

class Status(models.TextChoices):
    UNPROCESSED = " ", "unprocessed"
    UNSURE = "u", "unsure"
    ERROR = "e", "error"
    SPAM = "s", "spam"
    JAM = "j", "jam"

    @classmethod
    def style(cls, state):
        styles = {
            cls.UNPROCESSED: "table-secondary",
            cls.UNSURE: "table-secondary",
            cls.ERROR: "table-danger",
            cls.SPAM: "table-warning",
            cls.JAM: "table-info",
        }
        return styles.get(state, "table-dark")


class Website(models.Model):
    external_id = models.CharField(max_length=8)
    url = models.CharField(max_length=300)
    code = models.IntegerField(blank=True, null=True)
    score = models.IntegerField(blank=True, null=True)
    status = models.CharField(max_length=12, choices=Status.choices, default=Status.UNPROCESSED)

    def __str__(self):
        return self.url

    @property
    def style(self):
        return Status.style(self.status)

    def download(self):
        r = subprocess.run(["lynx", "--dump", self.url], capture_output=True)
        self.code = r.returncode
        if r.stderr:
            print(f"STDERR: \n{r.stderr}")
        return r.stdout

    def classify(self, content, option):
        states = {
                0: Status.SPAM,
                1: Status.JAM,
                2: Status.UNSURE,
                3: Status.ERROR,
        }
        r = subprocess.run(
            ["bogofilter", option],
            env={'BOGOFILTER_DIR': settings.BOGOFILTER_DIR},
            input=content,
            capture_output=True
        )
        self.status = states.get(r.returncode, Status.UNPROCESSED)
        stdout = r.stdout.decode("utf-8").strip()
        try:
            self.score = float(stdout.split(" ")[1]) * 100
        except:
            print(f"Error parsing bogofilter output. Leaving empty score. {stdout}")
            print(r.stderr)

    def process(self):
        content = self.download()
        if self.status == Status.UNPROCESSED:
            self.classify(content, "-tu")
        else:
            self.classify(content, "-t")
        self.save()

    def spam(self):
        if self.status == Status.SPAM:
            return
        content = self.download()
        self.classify(content, "-tNs")
        self.status = Status.SPAM
        self.save()

    def jam(self):
        if self.status == Status.JAM:
            return
        content = self.download()
        self.classify(content, "-tSn")
        self.status = Status.JAM
        self.save()

    @classmethod
    def unprocessed(cls):
        return cls.objects.exclude(status=Status.SPAM).exclude(status=Status.JAM)

class Binary(models.Model):
    class Meta:
        verbose_name_plural = "binaries"

    website = models.ForeignKey(Website, related_name="binaries", on_delete=models.CASCADE)
    raw = models.TextField()
    extracted = models.TextField()


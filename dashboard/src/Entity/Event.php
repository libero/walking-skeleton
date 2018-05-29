<?php

namespace Libero\Dashboard\Entity;

use DateTimeImmutable;
use DateTimeZone;
use Doctrine\ORM\Mapping as ORM;

/**
 * @ORM\Entity
 * @ORM\Table(uniqueConstraints={@ORM\UniqueConstraint(columns={"run", "type"})})
 */
final class Event
{
    /**
     * @ORM\Column(type="datetime_immutable")
     */
    private $dateTime;

    /**
     * @ORM\Column(type="guid")
     * @ORM\Id
     */
    private $id;

    /**
     * @ORM\Column(type="string", nullable=true)
     */
    private $message;

    /**
     * @ORM\Column(type="guid")
     */
    private $run;

    /**
     * @ORM\Column(type="string")
     */
    private $type;

    public function __construct(string $id, string $run, DateTimeImmutable $dateTime, string $type, ?string $message)
    {
        $this->id = $id;
        $this->run = $run;
        $this->dateTime = $dateTime->setTimezone(new DateTimeZone('UTC'));
        $this->type = $type;
        $this->message = $message;
    }

    public function getDateTime() : DateTimeImmutable
    {
        return $this->dateTime;
    }

    public function getId() : string
    {
        return $this->id;
    }

    public function getMessage() : ?string
    {
        return $this->message;
    }

    public function getRun() : string
    {
        return $this->run;
    }

    public function getType() : string
    {
        return $this->type;
    }
}
